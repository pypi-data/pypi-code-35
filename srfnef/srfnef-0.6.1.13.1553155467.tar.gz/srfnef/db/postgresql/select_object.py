# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: select_object.py
@date: 3/13/2019
@desc:
'''

from sqlalchemy.orm import sessionmaker

from srfnef.db import create_schema
from srfnef.typing import TYPE_BIND
from srfnef.utils import convert_snake_to_Camel, tqdm
from .config import engine, kw_exception

Session = sessionmaker(bind = engine)

session = Session()


def select_with_id(table_name, ids = None):
    if ids is None:
        return []
    if not isinstance(ids, list):
        ids = [ids]

    cls = TYPE_BIND[convert_snake_to_Camel(table_name)]
    table_cls_name = convert_snake_to_Camel(table_name) + 'Table'
    if table_cls_name in TYPE_BIND.keys():
        table_cls = TYPE_BIND[table_cls_name]
    else:
        create_schema(TYPE_BIND[convert_snake_to_Camel(table_name)])
        table_cls = TYPE_BIND[table_cls_name]
    outs = session.query(table_cls).filter(table_cls.id.in_(ids)).all()
    objs = []
    for out in outs:
        kwargs = {}
        for key, val in out.__dict__.items():
            if key == 'data':
                import numpy as np
                kwargs.update({key: np.load(val)})

            elif key.endswith('_id'):
                val_ = select_with_id(key[:-3], ids = val)
                kwargs.update({key[:-3]: val_})
            elif key not in kw_exception:
                kwargs.update({key: val})
            else:
                pass
        objs.append(cls(**kwargs))

    if len(ids) == 1:
        return objs[0]
    else:
        return objs


def run_task(table_names, ids, *, labels):
    from .add_object import add_object
    table_name1, table_name2 = table_names

    for id_pair in tqdm(ids):
        func = select_with_id(table_name1, id_pair[0])
        args = select_with_id(table_name2, id_pair[1])
        add_object(func(args, labels = labels), commit = True, labels = labels + ['final'])


def get_all_hash(table_name):
    table_cls_name = convert_snake_to_Camel(table_name) + 'Table'
    if table_cls_name in TYPE_BIND.keys():
        table_cls = TYPE_BIND[table_cls_name]
    else:
        create_schema(TYPE_BIND[convert_snake_to_Camel(table_name)])
        table_cls = TYPE_BIND[table_cls_name]
    outs = session.query(table_cls.hash_).all()
    return outs


def update_labels(table_name, ids, labels = [], mode = 'add'):
    if ids is None:
        return []
    if not isinstance(ids, list):
        ids = [ids]

    table_cls_name = convert_snake_to_Camel(table_name) + 'Table'
    if table_cls_name in TYPE_BIND.keys():
        table_cls = TYPE_BIND[table_cls_name]
    else:
        create_schema(TYPE_BIND[convert_snake_to_Camel(table_name)])
        table_cls = TYPE_BIND[table_cls_name]
    outs = session.query(table_cls).filter(table_cls.id.in_(ids)).all()
    for out in outs:
        if mode == 'add':
            out.labels = out.labels + labels
        elif mode == 'new':
            out.labels = labels
        else:
            raise ValueError
    session.commit()
