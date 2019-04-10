import threading

from hawkei.utils import merge

class Store():
    _store = None

    @classmethod
    def init(cls):
        cls._store = threading.local()
        cls._store.val = {}

    @classmethod
    def get(cls):
        try:
            return cls._store.val
        except AttributeError:
            return {}

    @classmethod
    def add(cls, attributes):
        try:
            cls._store.val = merge(cls._store.val, attributes)
            return cls._store.val
        except AttributeError:
            return {}

    @classmethod
    def clear(cls):
        try:
            cls._store.val = {}
            return cls._store.val
        except AttributeError:
            return {}

    @classmethod
    def delete(cls):
        cls.clear()
        del cls._store
