from .LazyUrlDataGetter import LazyUrlDataGetter
from .DataGetter import DataGetter


class LayersWrapper:
    """ The encapsulation of data layers
    Attributes:
        semantic_2d: a data_object.DataGetter object of sematic 2D
        dynamic_objects: a list of data_object.DataGetter objects of dynamic scenario
    """
    def __init__(self):
        self.semantic_2d = None
        self.dynamic_objects = []


class Dataset:
    """A dataset is the data unit which include different data layers.
    Attributes:
        id: identity of this dataset
        layers: layers in this dataset
    """
    def __init__(self, json_object):
        self.id = json_object["id"]
        self.layers = self.convert_json_layer(json_object["layers"])

    @staticmethod
    def convert_json_layer(json_layers):
        layers = LayersWrapper()
        if "semantic2D" in json_layers:
            layers.semantic_2d = DataGetter(json_layers["semantic2D"])
        if "dynamicObjects" in json_layers:
            for dynamc_object in json_layers["dynamicObjects"]:
                layers.dynamic_objects.append(LazyUrlDataGetter(dynamc_object["url"]))

        return layers
