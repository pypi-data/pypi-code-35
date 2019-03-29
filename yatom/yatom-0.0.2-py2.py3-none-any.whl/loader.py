import six
import yaml

try:
    from yaml import CBaseLoader as YamlLoaderBase
except ImportError:  # pragma: no-cover
    from yaml import BaseLoader as YamlLoaderBase


class YamlPairLoaderMeta(type):
    def __init__(self, name, bases, dct):
        super(YamlPairLoaderMeta, self).__init__(name, bases, dct)

        self.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            self._construct_mapping
            )

    @classmethod
    def _construct_mapping(cls, loader, node):
        return loader.construct_pairs(node)


class YamlPairLoader(six.with_metaclass(YamlPairLoaderMeta, YamlLoaderBase)):
    pass
