class Snapshot:
    def __init__(self, snapshot_number, entities, relations, attribute_map):
        self.__snapshot_number = snapshot_number
        self.__entities = entities
        self.__relations = relations
        self.__attribute_map = attribute_map

    @property
    def snapshot_number(self):
        return self.__snapshot_number

    @snapshot_number.setter
    def snapshot_number(self, snapshot_number):
        self.__snapshot_number = snapshot_number

    @property
    def entities(self):
        return self.__entities

    @entities.setter
    def entities(self, entities):
        self.__entities = entities

    @property
    def relations(self):
        return self.__relations

    @relations.setter
    def relations(self, relations):
        self.__relations = relations

    @property
    def attribute_map(self):
        return self.__attribute_map

    @attribute_map.setter
    def attribute_map(self, attribute_map):
        self.__attribute_map = attribute_map
