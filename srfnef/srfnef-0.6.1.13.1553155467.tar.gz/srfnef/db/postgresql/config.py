# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: config.py
@date: 3/13/2019
@desc:
'''
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from srfnef.utils import separator, main_path

engine = create_engine('postgresql://postgres:postgres@localhost/nef_db')

metadata = MetaData()

conn = engine.connect()

Base = declarative_base()

table_directory = main_path + 'db' + separator + 'tables' + separator
table_class_directory = main_path + 'db' + separator + 'table_classes' + separator

resource_directory = main_path + 'db' + separator + 'resources' + separator

kw_exception = ('_sa_instance_state', 'id', 'name', 'creator', 'labels', 'datetime', 'hash_')


def hasher_(dct: dict, exception = kw_exception):
    import hashlib
    m = hashlib.sha256()
    for key, val in dct.items():
        if key in exception:
            continue
        m.update(str(val).encode('utf-8'))
    return m.hexdigest()


def resource_hash_(path: str):
    import hashlib, os

    if os.path.isdir(path):
        raise ValueError('Only file can be hashed')

    def hash_(path):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()

        with open(path, 'rb') as fin:
            buf = fin.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = fin.read(BLOCKSIZE)
        return hasher.hexdigest()

    file_hashes = hash_(path)
    return ''.join(file_hashes)
