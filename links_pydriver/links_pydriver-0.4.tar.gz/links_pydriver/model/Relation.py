class Relation:
    def __init__(self, relationID, nodeAid, nodeBid, isOriented, type):
        self.__relationID = relationID
        self.__nodeAid = nodeAid
        self.__nodeBid = nodeBid
        self.__isOriented = isOriented
        self.__type = type

    @property
    def relationID(self):
        return self.__relationID

    @relationID.setter
    def relationID(self, relationID):
        self.__relationID = relationID

    @property
    def nodeAid(self):
        return self.__nodeAid

    @nodeAid.setter
    def nodeAid(self, nodeAid):
        self.__nodeAid = nodeAid

    @property
    def nodeBid(self):
        return self.__nodeBid

    @nodeBid.setter
    def nodeBid(self, nodeBid):
        self.__nodeBid = nodeBid

    @property
    def isOriented(self):
        return self.__isOriented

    @isOriented.setter
    def isOriented(self, isOriented):
        self.__isOriented = isOriented

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type
