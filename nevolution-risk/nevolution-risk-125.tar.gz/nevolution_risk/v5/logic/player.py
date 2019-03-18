import numpy as np
from numpy import float32

from nevolution_risk.constants.colors import white
from nevolution_risk.v5.logic.card import Card
from nevolution_risk.v3.logic import Graph


class Player(object):
    def __init__(self, name, troops=0, color=white, action_len=0):
        self.name = name
        self.troops = troops
        self.color = color
        self.valid_actions = np.zeros(action_len, dtype=float32)
        self.cards = []
        self.card = Card()

    def add_card(self):
        """
        Creates a card and adds it to the list cards
        :return:
        """
        card = self.card.area_card()
        self.cards.append(card)

    def redeem_infa_area_card(self, node):
        """
        Checks if the player has three or more infantry cards (= 1) in his deck, adds then 4 troop units to the
        chosen node and removes three infantry cards from his deck
        :param node: integer, node that will get the troops
        :return: returns false if player has three or less infantry cards in his deck
        """
        infa = self.cards.count(self.card.infantry)
        if infa >= 3:
            graph.nodes[node].troops = graph.nodes[node].troops + 4
            var = 3
            for elem in self.cards[:]:
                if elem == self.card.infantry and var != 0:
                    self.cards.remove(elem)
                    var = var - 1
        return False

    def redeem_cava_area_card(self, node):
        """
        Checks if the player has three or more cavalry cards (= 2) in his deck, adds then 6 troop units to the
        chosen node and removes three cavalry cards from his deck
        :param node: integer, node that will get the troops
        :return: returns false if player has three or less cavalry cards in his deck
        """
        cava = self.cards.count(self.card.cavalry)
        if cava >= 3:
            graph.nodes[node].troops = graph.nodes[node].troops + 6
            var = 3
            for elem in self.cards[:]:
                if elem == self.card.cavalry and var != 0:
                    self.cards.remove(elem)
                    var = var - 1
        return False

    def redeem_arti_area_card(self, node):
        """
        Checks if the player has three or more artillery cards (= 3) in his deck, adds then 8 troop units to the
        chosen node and removes three artillery cards from his deck
        :param node: integer, node that will get the troops
        :return: returns false if player has three or less artillery cards in his deck
        """
        arti = self.cards.count(self.card.artillery)
        if arti >= 3:
            graph.nodes[node].troops = graph.nodes[node].troops + 8
            var = 3
            for elem in self.cards[:]:
                if elem == self.card.artillery and var != 0:
                    self.cards.remove(elem)
                    var = var - 1
        return False

    def redeem_mixed_area_card(self, node):
        """
        Checks if the player has three different kind of cards (= 1, 2, 3) in his deck, adds then 10 troop units to the
        chosen node and removes these cards from his deck
        :param node: integer, node that will get the troops
        :return: returns false if player has not three different kind of cards
        """
        infa = self.cards.count(self.card.infantry)
        cava = self.cards.count(self.card.cavalry)
        arti = self.cards.count(self.card.artillery)
        if infa >= 1 and cava >= 1 and arti >= 1:
            graph.nodes[node].troops = graph.nodes[node].troops + 10
            self.cards.remove(self.card.infantry)
            self.cards.remove(self.card.cavalry)
            self.cards.remove(self.card.artillery)


if __name__ == '__main__':
    graph = Graph((1, 2), 2)
    player = Player("dirk")

    graph.nodes[23].player = player
    graph.nodes[23].troops = 4

    player.add_card()
    player.add_card()
    player.add_card()
    player.add_card()
    player.add_card()

    print(player.cards, "<<< player", " counting", player.card.infantry, ">>", player.cards.count(player.card.infantry))
    print(player.cards, "<<< player", " counting", player.card.cavalry, ">>", player.cards.count(player.card.cavalry))
    print(player.cards, "<<< player", " counting", player.card.artillery, ">>", player.cards.count(player.card.artillery))

    print("troops on node >>>",graph.nodes[23].troops)

    player.redeem_mixed_area_card(23)

    print(player.cards, "<<< player", " counting", player.card.infantry, ">>", player.cards.count(player.card.infantry))
    print(player.cards, "<<< player", " counting", player.card.cavalry, ">>", player.cards.count(player.card.cavalry))
    print(player.cards, "<<< player", " counting", player.card.artillery, ">>", player.cards.count(player.card.artillery))

    print("troops on node after using cards >>>",graph.nodes[23].troops)