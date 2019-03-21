import numpy as np
from numpy import float32

from nevolution_risk.constants.colors import white
from nevolution_risk.v4.logic.card_factory import Card_factory


class Player(object):
    def __init__(self, name, id=0, color=white, action_len=0, card_factory=None):
        self.name = name
        self.id = id
        self.troops = 0
        self.color = color
        self.valid_actions = np.zeros(action_len, dtype=float32)
        self.card_factory = None
        self.card_received = False

        if card_factory is None:
            self.card_factory = Card_factory()
        else:
            self.card_factory = card_factory

        self.reward = 0
        self.next_player = None
        self.lost = False
        self.cards = []

    def add_card(self):
        """
        Adds a card to the player card deck
        :return:
        """
        self.cards.append(self.card_factory.area_card())

    def combine_cards(self):
        """
        Combines player cards depending on how many of kind of cards the player holds in his deck
        :return: adds, depending on the combination, 4, 6, 8 or 10 troops to the player troops
        """
        i = 0
        c = 0
        a = 0
        for card in self.cards:
            if card.typ == 0:
                i = i + 1
            elif card.typ == 1:
                c = c + 1
            elif card.typ == 2:
                a = a + 1

        for card in self.cards:
            if i > 0 and c > 0 and a > 0:
                var1 = 1
                var2 = 1
                var3 = 1
                for ele in self.cards[:]:
                    if ele.typ == 0 and var1 != 0:
                        self.cards.remove(ele)
                        var1 = var1 - 1
                    elif ele.typ == 1 and var2 != 0:
                        self.cards.remove(ele)
                        var2 = var2 - 1
                    elif ele.typ == 2 and var3 != 0:
                        self.cards.remove(ele)
                        var3 = var3 - 1

                    if var1 == 0 and var2 == 0 and var3 == 0:
                        self.troops += 10
                        return True


            elif card.typ == 0:
                if i >= 3:
                    n = 3
                    for ele in self.cards[:]:
                        if ele.typ == 0:
                            self.cards.remove(ele)
                            n = n - 1
                            if n == 0:
                                self.troops += 4
                                return True
            elif card.typ == 1:
                if c >= 3:
                    n = 3
                    for ele in self.cards[:]:
                        if ele.typ == 1:
                            self.cards.remove(ele)
                            n = n - 1
                            if n == 0:
                                self.troops += 6
                                return True
            elif card.typ == 2:
                if a >= 3:
                    n = 3
                    for ele in self.cards[:]:
                        if ele.typ == 2:
                            self.cards.remove(ele)
                            n = n - 1
                            if n == 0:
                                self.troops += 8
                                return True
            else:
                return False
        return False


"""
    def redeem_infa_area_card(self, card_infa):
        Checks if the player has three or more cavalry cards (= 0) in his deck, adds then 6 troop units to the
        chosen node and removes three cavalry cards from his deck
        :param card_cava: object card
        :param node: integer, node that will get the troops
        :return: returns false if player has three or less cavalry cards in his deck
        infa = self.cards.count(card_infa.typ)

        if infa >= 3 and card_infa.typ == 0:
            self.troops = self.troops + 4
            var = 3
            for elem in self.cards[:]:
                if elem == card_infa and var != 0:
                    self.cards.remove(elem)
                    var = var - 1
        return False

    def redeem_cava_area_card(self, card_cava):
        Checks if the player has three or more cavalry cards (= 1) in his deck, adds then 6 troop units to the
        chosen node and removes three cavalry cards from his deck
        :param card_cava: object card
        :param node: integer, node that will get the troops
        :return: returns false if player has three or less cavalry cards in his deck
        cava = self.cards.count(card_cava)
        if cava >= 3 and card_cava.typ == 1:
            self.troops = self.troops + 6
            var = 3
            for elem in self.cards[:]:
                if elem == card_cava and var != 0:
                    self.cards.remove(elem)
                    var = var - 1
        return False

    def redeem_arti_area_card(self, card_arti):
        Checks if the player has three or more artillery cards (= 2) in his deck, adds then 8 troop units to the
        chosen node and removes three artillery cards from his deck
        :param card_arti: object card
        :param node: integer, node that will get the troops
        :return: returns false if player has three or less artillery cards in his deck
        arti = self.cards.count(card_arti)
        if arti >= 3 and card_arti.typ == 2:
            self.troops = self.troops + 8
            var = 3
            for elem in self.cards[:]:
                if elem == card_arti and var != 0:
                    self.cards.remove(elem)
                    var = var - 1
        return False

    def redeem_mixed_area_card(self, card_infa, card_cava, card_arti):
        Checks if the player has three different kind of cards (= 0, 1, 2) in his deck, adds then 10 troop units to the
        chosen node and removes these cards from his deck
        :param card_infa: object card infantry
        :param card_cava: object card cavalry
        :param card_arti: object card artillery
        :param node: integer, node that will get the troops
        :return: returns false if player has not three different kind of cards
        infa = self.cards.count(card_infa)
        cava = self.cards.count(card_cava)
        arti = self.cards.count(card_arti)
        if infa >= 1 and cava >= 1 and arti >= 1 and card_infa == 0 and card_cava == 1 and card_arti == 2:
            player.troops = player.troops + 10
            self.cards.remove(card_infa)
            self.cards.remove(card_cava)
            self.cards.remove(card_arti)
"""

if __name__ == '__main__':
    # graph = Graph((1, 2), 4)
    # player = Player("dirk")

    # card = graph.card_fac.area_card()

    # player.add_card()
    # player.add_card()
    # player.add_card()
    # player.add_card()
    # player.add_card()

    # print("\n", player.cards, "\n")

    # print(player.combine_cards())

    # print("\n", player.cards, "\n")
    pass
