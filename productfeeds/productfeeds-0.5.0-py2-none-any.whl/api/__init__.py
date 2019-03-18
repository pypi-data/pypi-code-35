from abc import abstractmethod, abstractproperty, ABCMeta


class AbstractImporterAPIException(Exception):
    pass


class AbstractImporterAPI:
    __metaclass__ = ABCMeta

    def __init__(self, articlecode_prefix='', *args, **kwargs):
        self.prefix = articlecode_prefix
        try:
            self.storage = kwargs['storage']
        except KeyError:
            self.storage = None

        self.prefix = articlecode_prefix
        try:
            self.tmp_dir = kwargs['tmp_dir']
        except KeyError:
            self.tmp_dir = ''

    def _build_articlecode(self, product_id):
        prefix = ''
        if self.prefix:
            prefix = self.prefix

        return "{}{}".format(prefix, product_id)

    @abstractmethod
    def import_products(self):
        pass

    def _save_product(self, p):
        if self.storage is not None:
            self.storage.save_product(p)

