class Continent(object):

    def __init__(self, id, nodes):
        self.reward_level = 0
        self.nodes = nodes
        self.id = id

        for node in nodes:
            node.continent = self

        if self.id == 0:
            self.init(2)
        elif self.id == 1:
            self.init(1)
        elif self.id == 2:
            self.init(2)
        elif self.id == 3:
            self.init(1)
        elif self.id == 4:
            self.init(3)
        elif self.id == 5:
            self.init(1)

    def reward(self):
        # TODO: revisit rewards (delete TODO if rewards are fine) and comment
        return self.reward_level

    def init(self, lvl):
        # TODO: comment
        self.reward_level = lvl
