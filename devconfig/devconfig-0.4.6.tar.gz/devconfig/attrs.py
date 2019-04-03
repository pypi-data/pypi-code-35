import yaml.nodes
class YamlAttributedObject(object):
    @classmethod
    def from_yaml_node(cls, loader, node):
        if isinstance(node, yaml.nodes.MappingNode):
            return cls(**loader.construct_mapping(node, deep=True))
        elif isinstance(node, yaml.nodes.SequenceNode):
            return cls(*loader.construct_sequence(node, deep=True))
        elif isinstance(node, yaml.nodes.ScalarNode):
            return cls(loader.construct_object(node, deep=True))
