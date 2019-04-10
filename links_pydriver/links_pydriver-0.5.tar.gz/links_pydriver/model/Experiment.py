class Experiment:
    def __init__(self, experimentName, attributeMap, snapshots):
        self.__experimentName = experimentName
        self.__attributeMap = attributeMap
        self.__snapshots = snapshots

    @property
    def experimentName(self):
        return self.__experimentName

    @experimentName.setter
    def experimentName(self, experimentName):
        self.__experimentName = experimentName

    @property
    def attributeMap(self):
        return self.__attributeMap

    @attributeMap.setter
    def attributeMap(self, attributeMap):
        self.__attributeMap = attributeMap

    @property
    def snapshots(self):
        return self.__snapshots

    @snapshots.setter
    def snapshots(self, snapshots):
        self.__snapshots = snapshots
