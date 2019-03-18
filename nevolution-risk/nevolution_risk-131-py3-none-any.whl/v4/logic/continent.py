class Continent(object):

    def __init__(self, id, nodes):
        self.reward_level = 0
        self.nodes = nodes
        self.id = id
        # id's -> continent
        # 0 -> Nord-Amerika
        # 1 -> Süd-Amerika
        # 2 -> Europa
        # 3 -> Afrika
        # 4 -> Asien
        # 5 -> Ozeanien

        for node in nodes:
            node.continent = self

        self.init()

    def reward(self):
        """
        Interprets the reward_level to an equivalent of troop units

        :return: integer, number of troop units
        """
        troops = 0
        if self.reward_level == 1:
            troops = 2
        elif self.reward_level == 2:
            troops = 3
        elif self.reward_level == 3:
            troops = 5
        elif self.reward_level == 4:
            troops = 7
        return troops

    def init(self):
        """
        Gives every continent a spezific reward_level

        :return: None
        """
        if self.id == 0:
            self.reward_level = 3
        elif self.id == 1:
            self.reward_level = 1
        elif self.id == 2:
            self.reward_level = 3
        elif self.id == 3:
            self.reward_level = 2
        elif self.id == 4:
            self.reward_level = 4
        elif self.id == 5:
            self.reward_level = 1
