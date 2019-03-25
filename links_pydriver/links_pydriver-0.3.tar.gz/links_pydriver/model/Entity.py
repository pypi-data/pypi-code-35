class Entity():
    def __init__(self, entityID, type, attribute_map):
        self.__entityID = entityID
        self.__type = type
        self.__attribute_map = attribute_map

    @property
    def entityID(self):
        return self.__entityID

    @entityID.setter
    def entityID(self, entityID):
        self.__entityID = entityID

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def attribute_map(self):
        return self.__attribute_map

    @attribute_map.setter
    def attribute_map(self, attribute_map):
        self.__attribute_map = attribute_map

