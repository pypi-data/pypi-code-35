from random import Random

from nevolution_risk.v4.logic.card import Card


class Card_factory(object):

    def __init__(self, seed=42):
        self.seed = seed
        self.random = Random(self.seed)

    def area_card(self):
        """
        Creates a random number (card)
        :return: returns the object Card
        """
        random_value = self.random.randint(0, 2)
        return Card(random_value)


if __name__ == '__main__':
    pass
