# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: add_object.py
@date: 3/12/2019
@desc:
'''
import time
import typing
from getpass import getuser

import numpy as np
from sqlalchemy.orm import sessionmaker

from srfnef.typing import DataClass, TYPE_BIND
from .config import engine, resource_directory, hasher_, resource_hash_

Session = sessionmaker(bind = engine)

session = Session()


def add_object(obj: DataClass, *, labels = [], commit = False, hash_unique_check = True):
    table_class_name = obj.__class__.__name__ + 'Table'
    if table_class_name in TYPE_BIND.keys():
        table_cls = TYPE_BIND[table_class_name]
    else:
        from .create_schema import create_schema
        table_cls = create_schema(obj.__class__, commit = commit)

    kwargs = {'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))}
    kwargs.update({'creator': getuser()})
    kwargs.update({'labels': labels})
    hash_dict = {}
    for key, val in obj.__class__.fields().items():
        if key == 'data':
            _id = str(time.time()).replace('.', '')
            if isinstance(getattr(obj, key), np.ndarray):
                np.save(resource_directory + _id + '.npy', getattr(obj, key))
                kwargs.update({key: resource_directory + _id + '.npy'})

                hash_dict.update({'data': resource_hash_(resource_directory + _id + '.npy')})
            else:
                raise NotImplementedError
        else:
            if val.type is typing.List[float] or val.type is typing.List[int]:
                val_ = getattr(obj, key)
                if isinstance(val_, np.ndarray):
                    if val_.dtype in (np.int32, np.int64):
                        val_ = val_.tolist()
                    elif val_.dtype in (np.float32, np.float64):
                        val_ = val_.tolist()
                    else:
                        raise NotImplementedError
                try:
                    kwargs.update({key: val_})
                except:
                    raise NotImplementedError(f'type {type(val_)} is not implemented yet')

                hash_val = val_
            elif val.type.__name__ + 'Table' in TYPE_BIND.keys():
                sub_, hash_val = add_object(getattr(obj, key), labels = labels, commit =
                commit)
                kwargs.update({key: sub_})
            else:
                val_ = getattr(obj, key)
                if isinstance(val_, np.int64):
                    val_ = int(val_)
                elif isinstance(val_, np.float32):
                    val_ = float(val_)
                try:
                    kwargs.update({key: val_})
                except:
                    raise NotImplementedError(f'type {type(val_)} is not implemented yet')
                hash_val = val_
            hash_dict.update({key: hash_val})

    hash_ = hasher_(hash_dict)
    kwargs.update({'hash_': hash_})
    table_obj = table_cls(**kwargs)

    if commit:
        session.add(table_obj)
        session.commit()
    return table_obj, hash_
