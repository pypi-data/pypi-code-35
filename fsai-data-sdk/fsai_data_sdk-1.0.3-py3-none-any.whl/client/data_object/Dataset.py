from .LazyUrlDataObject import LazyUrlDataObject
from .DataObject import DataObject


class Layers:
    def __init__(self):
        self.semantic_2d = None
        self.dynamic_objects = []


class Dataset:
    def __init__(self, json_object):

        self.layers = Layers()
        layers = json_object["layers"]
        if "semantic2D" in layers:
            self.layers.semantic_2d = DataObject(layers["semantic2D"])
        if "dynamicObjects" in layers:
            self.dynamic_objects = []
            for dynamc_object in layers["dynamicObjects"]:
                self.layers.dynamic_objects.append(LazyUrlDataObject(dynamc_object["url"]))

