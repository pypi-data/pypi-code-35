import yaml

from qsa.lib.datastructures import DTO
from qsa.lib.datastructures import ImmutableDTO


def represent_ordereddict(dumper, data):
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


class Base64DER(str):

    @classmethod
    def represent(self, dumper, data):
        """Represents the base64-encoded DER string as YAML."""
        return dumper.represent_scalar('tag:yaml.org,2002:str',
            data, style='|')

    @classmethod
    def fromfile(cls, src):
        return cls(open(src).read())


class SerializedDatastructure(str):

    @classmethod
    def new(cls, serializable):
        return cls(yaml.safe_dump(serializable, indent=2,
            default_flow_style=False))

    @classmethod
    def represent(self, dumper, data):
        """Represents the base64-encoded DER string as YAML."""
        return dumper.represent_scalar('tag:yaml.org,2002:str',
            data, style='|')


yaml.add_representer(Base64DER, Base64DER.represent,
    Dumper=yaml.SafeDumper)
yaml.add_representer(DTO, represent_ordereddict,
    Dumper=yaml.SafeDumper)
yaml.add_representer(ImmutableDTO, represent_ordereddict,
    Dumper=yaml.SafeDumper)
yaml.add_representer(SerializedDatastructure, SerializedDatastructure.represent,
    Dumper=yaml.SafeDumper)
