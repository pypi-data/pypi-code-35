import sys
import logging
import yaml
from collections.abc import Mapping
from collections import ChainMap

class NestedChainMap(ChainMap):
    def __getitem__(self, name):
        value = super(self.__class__, self).__getitem__(name)
        if isinstance(value, self.__class__):
            return value

        contexts = [m.get(name) for m in self.maps if name in m]

        if all((isinstance(ctx, Mapping) for ctx in contexts)):
            return self.__class__(*contexts)
        elif isinstance(contexts[0], Mapping):
            return self.__class__(*(c for c in contexts if isinstance(c, Mapping)))
        else:
            return contexts[0]

    def as_dict(self):
        mapping = {}
        for k, v in list(self.items()):
            if isinstance(v, self.__class__):
                mapping[k] = v.as_dict()
            else:
                mapping[k] = v
        return mapping

def mappings(*mappings):
    '''
    Merges `*mappings` list with priority to last item
    '''
    return NestedChainMap(*(reversed(mappings))).as_dict()


def _common_mapping_values(src, dest):
    for src_key, src_value in src.value:
        for dest_key, dest_value in dest.value:
            if src_key.value == dest_key.value:
                yield src_value, dest_value

def _extra_items(src, dest):
    items = []
    for src_key, src_value in src.value:
        for dest_key, dest_value in dest.value:
            if src_key.value == dest_key.value:
                break
        else:
            items.append((src_key, src_value)) 
    return items


def extend_node(src, dest):
    """
    Recursively update dest mapping nodes with extra nodes from src

    """
    if not isinstance(dest, yaml.MappingNode) or not isinstance(src, yaml.MappingNode):
        return dest
    for src_mapping, dest_mapping in _common_mapping_values(src, dest):
        extend_node(src_mapping, dest_mapping)
    dest.value = dest.value + _extra_items(src, dest)