class Experiment:
    def __init__(self, name, attribute_map, snapshots):
        self.__name = name
        self.__attribute_map = attribute_map
        self.__snapshots = snapshots

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def attribute_map(self):
        return self.__attribute_map

    @attribute_map.setter
    def attribute_map(self, attribute_map):
        self.__attribute_map = attribute_map

    @property
    def snapshots(self):
        return self.__snapshots

    @snapshots.setter
    def snapshots(self, snapshots):
        self.__snapshots = snapshots
