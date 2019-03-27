class Snapshot:
    def __init__(self, snapshotNumber, entities, relations, attributeMap):
        self.__snapshotNumber = snapshotNumber
        self.__entities = entities
        self.__relations = relations
        self.__attributeMap = attributeMap

    @property
    def snapshotNumber(self):
        return self.__snapshotNumber

    @snapshotNumber.setter
    def snapshotNumber(self, snapshotNumber):
        self.__snapshotNumber = snapshotNumber

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
    def attributeMap(self):
        return self.__attributeMap

    @attributeMap.setter
    def attributeMap(self, attributeMap):
        self.__attributeMap = attributeMap
