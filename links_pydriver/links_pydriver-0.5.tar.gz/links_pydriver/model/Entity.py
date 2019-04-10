class Entity():
    def __init__(self, entityID, type, attributeMap):
        self.__entityID = entityID
        self.__type = type
        self.__attributeMap = attributeMap

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
    def attributeMap(self):
        return self.__attributeMap

    @attributeMap.setter
    def attributeMap(self, attributeMap):
        self.__attributeMap = attributeMap
