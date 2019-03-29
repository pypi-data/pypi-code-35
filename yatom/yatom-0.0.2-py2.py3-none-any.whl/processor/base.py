import six
import yaml

import yatom.loader as loader


class ProcessError(yaml.YAMLError):
    pass


class BaseProcessorMeta(type):
    '''
    Makes attrs and nodes class attribute dict values to point to
    attr_ and node_ methods, respectively, also applying inheritance
    to said dict contents.
    '''
    def __init__(self, name, bases, dct):
        super(BaseProcessorMeta, self).__init__(name, bases, dct)

        # apply smart inheritance of handler dicts
        for category in ('attrs', 'nodes'):
            handlers = {}
            handler_prefix = '{}_'.format(category[:-1])
            for cls in self.mro()[::-1]:
                # handlers by method name
                handlers.update(
                    (name[5:].replace('_', '-'), name)
                    for name in cls.__dict__ if name.startswith(handler_prefix)
                    )
                # handlers defined by hand
                handlers.update(getattr(cls, category, {}))
            setattr(self, category, handlers)


class BaseProcessor(six.with_metaclass(BaseProcessorMeta)):
    yaml_loader = loader.YamlPairLoader
    attrs = {}
    nodes = {}

    def __init__(self, tree):
        self.tree = tree

    def process_node(self, name, value):
        for node in value:
            if self._is_nonstr_iterable(node):
                yield '%r: %r' % (name, value) if value else name
                continue
            for txt in self.process_value(*node):
                yield txt

    def process_value(self, value):
        for name, value in value:
            for txt in self.process_node(name, value):
                yield txt

    def render(self):
        return ''.join(self.process_value(self.tree))

    @classmethod
    def _is_nonstr_iterable(cls, x):
        return hasattr(x, '__iter__') and not isinstance(x, six.string_types)

    @classmethod
    def from_file(cls, file):
        assert callable(getattr(file, 'read', None)), \
            ValueError('%s.from_file expects a readable file' % cls.__name__)
        data = yaml.load(file, Loader=cls.yaml_loader)
        return cls(data)

    @classmethod
    def from_source(cls, data):
        assert isinstance(data, six.string_types), \
            ValueError('%s.from_source expects an str' % cls.__name__)
        data = yaml.load(data, Loader=cls.yaml_loader)
        return cls(data)
