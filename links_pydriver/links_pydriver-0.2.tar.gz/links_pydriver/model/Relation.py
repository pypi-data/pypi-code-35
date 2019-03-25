class Relation:
    def __init__(self, relationID, nodeAid, nodeBid, is_oriented, type):
        self.__relationID = relationID
        self.__nodeAid = nodeAid
        self.__nodeBid = nodeBid
        self.__is_oriented = is_oriented
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
    def is_oriented(self):
        return self.__is_oriented

    @is_oriented.setter
    def is_oriented(self, is_oriented):
        self.__is_oriented = is_oriented

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type
