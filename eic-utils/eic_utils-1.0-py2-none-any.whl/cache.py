import os, pickle, json
from .base import *

def __read__(f):
    return f.read()

def __write__(data, f):
    f.write('{}'.format(data))

def __write_bin__(data, f):
    f.write(data)

__file_op__ = {
    'str': {
        'name': 'str', 'r': 'r', 'w': 'w', 
        'load': __read__, 'dump': __write__,
    }, 
    'pkl': {
        'name': 'pickle', 'r': 'rb', 'w': 'wb', 
        'load': pickle.load, 'dump': pickle.dump,
    },
    'json': {
        'name': 'json', 'r': 'r', 'w': 'w',
        'load': json.load, 'dump': json.dump,
    },
    'bin': {
        'name': 'bin', 'r': 'rb', 'w': 'wb',
        'load': __read__, 'dump': __write_bin__,
    },
}

class Cache(object):
    def __init__(self, path, *,\
            default='pkl', file_op=__file_op__, extra={}):
        '''
        @params:
            path (str): path to store cache

            default (str): default value 'pkl'
                choices: file_op

            file_op (dict): file operations
                default: __file_op__
                key: r, w, load, dump
                instance: see dump(), load() for more details

            extra (dict): extra file_op to append
                default: {}

        @returns:
            instance of class
        '''
        self.path=path
        self.default=default  
        assert default in file_op, \
                '{} not in {}'.format(default, file_op.keys())
        self.file_op = __file_op__
        self.file_op.update(extra)
        touchdir(path)

    def items(self):
        return sorted(os.listdir(self.path))

    def remove(self, name):
        path = os.path.join(self.path, name)
        if os.path.isfile(path):
            os.remove(path)

    def dump(self, data, name, *, force=False, file_type=None):
        ''' 
        @params:
            data: data to save
            name (str): save path
            file_type (str): type of cache
                default: self.default
                default choices: str, json, pkl, bin
                instance:
                    file_op = self.file_op[file_type]
                    with open(name, file_op['w']) as f:
                        file_op['dump'](data, f)
        @returns:
            None
        '''
        if not file_type:
            file_type=self.default
        assert file_type in self.file_op.keys(),\
                '[ERR] key error: {} not found in {}'.\
                format(file_type, list(self.file_op.keys()))

        path = os.path.join(self.path, name)
        assert force or not os.path.isfile(path),\
                '{} exists, use force=True to overwrite'.format(name)
        touchdir(os.path.dirname(path))
        file_op = self.file_op[file_type]
        with open(path, file_op['w']) as f:
            file_op['dump'](data, f)

    def load(self, name, file_type=None):
        '''
        @params:
            name (str): save path
            file_type (str): type of cache
                default: self.default
                default choices: str, json, pkl
                instance:
                    file_op = self.file_op[file_type]
                    with open(name, file_op['r']) as f:
                        return file_op['load'](f)
        @returns:
            None
        '''
        if not file_type:
            file_type=self.default
        assert file_type in self.file_op.keys(),\
                '[ERR] key error: {} not found in {}'.\
                format(file_type, list(self.file_op.keys()))

        name = os.path.join(self.path, name)
        if not file_stat(name):
            return None

        file_op = self.file_op[file_type]
        with open(name, file_op['r']) as f:
            return file_op['load'](f)

