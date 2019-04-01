import ruamel.yaml


class YamlLoader:
    """A wrapper class that wraps loading of ordered yaml"""
    @staticmethod
    def ordered_load(stream):
        return ruamel.yaml.load(stream, Loader=ruamel.yaml.RoundTripLoader)
