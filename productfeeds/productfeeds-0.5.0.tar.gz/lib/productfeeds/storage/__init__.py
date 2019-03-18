from abc import abstractmethod, ABCMeta


class AbstractStorageException(Exception):
    pass


class AbstractStorage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_product(self, product):
        pass
