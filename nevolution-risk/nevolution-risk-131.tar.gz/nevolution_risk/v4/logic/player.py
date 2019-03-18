import numpy as np
from numpy import float32

from nevolution_risk.constants.colors import white


class Player(object):
    def __init__(self, name, id=0, color=white, action_len=0):
        self.name = name
        self.id = id
        self.troops = 0
        self.color = color
        self.valid_actions = np.zeros(action_len, dtype=float32)
        self.card_received = False
        self.reward = 0
        self.next_player = None
        self.lost = False

    def add_card(self):
        # TODO: implement
        pass

    def combine_cards(self):
        # TODO: implement
        pass


if __name__ == '__main__':
    for i in range(0, 4):
        print(i)
