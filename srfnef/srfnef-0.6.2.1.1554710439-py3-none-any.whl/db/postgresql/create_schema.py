# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: add_object.py
@date: 3/12/2019
@desc:
'''

import typing

from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from srfnef.typing import TYPE_BIND, DataClass
from srfnef.utils import convert_Camal_to_snake
from .config import engine, Base


def create_schema(cls: type, *, commit = False):
    table_name = convert_Camal_to_snake(cls.__name__)
    table_class_name = cls.__name__ + 'Table'
    if table_class_name in TYPE_BIND.keys():
        table_cls = TYPE_BIND[table_class_name]
    else:
        kwargs = {'__tablename__': table_name, 'id': Column(Integer, primary_key = True)}
        kwargs.update(({'datetime': Column(String)}))
        kwargs.update(({'creator': Column(String)}))
        kwargs.update({'labels': Column(postgresql.ARRAY(String, dimensions = 1))})
        for key, val in cls.fields().items():
            if key == 'data':
                kwargs.update({'data': Column(String)})
            else:
                if val.type is int:
                    kwargs.update({key: Column(Integer)})
                elif val.type is float:
                    kwargs.update({key: Column(Float)})
                elif val.type is bool:
                    kwargs.update({key: Column(Boolean)})
                elif val.type is str:
                    kwargs.update({key: Column(String)})
                elif val.type is typing.List[float]:
                    kwargs.update({key: Column(postgresql.ARRAY(Float, dimensions = 1))})
                elif val.type is typing.List[int]:
                    kwargs.update({key: Column(postgresql.ARRAY(Integer, dimensions = 1))})
                elif val.type is typing.List[str]:
                    kwargs.update({key: Column(postgresql.ARRAY(String, dimensions = 1))})
                elif val.type.__name__ + 'Table' in TYPE_BIND.keys():
                    kwargs.update({key + '_id': Column(Integer, ForeignKey(key + '.id'))})
                    kwargs.update({key: relationship(val.type.__name__ + 'Table')})
                elif issubclass(val.type, DataClass):
                    create_schema(val.type, commit = commit)
                    kwargs.update({key + '_id': Column(Integer, ForeignKey(key + '.id'))})
                    kwargs.update({key: relationship(val.type.__name__ + 'Table')})
                else:
                    raise NotImplementedError(f'type {val.type} is not implemented yet.')
        kwargs.update({'hash_': Column(String)})
        table_cls = type(table_class_name, (Base,), kwargs)
    TYPE_BIND.update({table_class_name: table_cls})

    if commit:
        Base.metadata.bind = engine
        Base.metadata.create_all()
    return table_cls
