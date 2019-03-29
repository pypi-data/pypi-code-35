# coding:utf-8

import random


class Poker(object):
    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8',
              '9', 'T', 'J', 'Q', 'K', 'joker', 'Joker']
    SUITS = ['♥', '♠', '♣', '♦', 'JOKER']
    JOKER = 'JOKER'

    def __init__(self, value='Joker', suit=SUITS[-1]):
        """允许传入牌面大小、花色的字符串，也接受传入牌面大小、花色对应序号"""
        if isinstance(value, int) and 0 <= value < len(Poker.VALUES):
            self.value = value
        elif value in Poker.VALUES:
            self.value = Poker.VALUES.index(value)
        else:
            raise Exception(f'Invalid poker value {type(value)}: {value}')

        if isinstance(suit, int) and 0 <= suit < len(Poker.SUITS):
            self.suit = suit
        elif suit in Poker.SUITS:
            self.suit = Poker.SUITS.index(suit)
        else:
            raise Exception(f'Invalid poker suit {type(suit)}: {suit}')

        if not self.is_joker() and self.get_suit() == Poker.JOKER:
            raise Exception(
                f'Invalid poker. Value [{self.get_value()}]. Suit [{self.get_suit()}]')

    def __str__(self):
        if self.suit < len(Poker.SUITS) - 1:
            return f'{Poker.SUITS[self.suit]}{Poker.VALUES[self.value]}'
        return Poker.VALUES[self.value]

    def __lt__(self, poker):
        return self.value < poker.value

    def __le__(self, poker):
        return self.value <= poker.value

    def __gt__(self, poker):
        return self.value > poker.value

    def __ge__(self, poker):
        return self.value >= poker.value

    def __eq__(self, poker):
        return self.value == poker.value

    def __ne__(self, poker):
        return self.value != poker.value

    def get_value(self):
        return Poker.VALUES[self.value]

    def get_suit(self):
        return Poker.SUITS[self.suit]

    def is_joker(self):
        return len(Poker.VALUES) - 3 < self.value < len(Poker.VALUES)


def is_joker(value):
    """判断牌面大小序号或牌对象是否为鬼牌"""
    if isinstance(value, Poker):
        return value.is_joker()
    if isinstance(value, int):
        return len(Poker.VALUES) - 2 < value < len(Poker.VALUES) - 1
    return value.upper() == Poker.JOKER


def create_pack(shuffled=True, with_joker=True):
    """创建一副牌"""
    pack = []
    for value in Poker.VALUES:
        if is_joker(value):
            if with_joker:
                pack.append(Poker(value))
            continue
        for suit in Poker.SUITS[:-1]:
            pack.append(Poker(value, suit))
    if shuffled:
        random.shuffle(pack)
    return pack


def display(poker_list, sep=' '):
    """展示一组牌"""
    result = sep.join(str(poker) for poker in poker_list)
    return result
