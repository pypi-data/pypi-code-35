# -*- coding: utf-8 -*-

# Copyright (C) 2019 github.com/shyal
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
from collections import OrderedDict
from traceback import print_exc

from api import FlashcardAlgorithm
from store import Cards, Card
from prefs import prefs, reset_prefs
from store import get_session

class VulcanModel(object):

    def __init__(self, db_path):
        self.session = get_session(db_path)
        self.refresh_tags()
        self.__current_card = None

    def refresh_tags(self):
        self.tags = OrderedDict()
        for tag in sorted(Cards.tags()):
            try:
                self.tags[tag] = prefs.get("tag_"+tag, True)
            except:
                # shelve sucks
                pass
        self.init_algo()

    @property
    def current_tags(self):
        return [k for k, v in self.tags.items() if v]

    def init_algo(self):
        self.algo = FlashcardAlgorithm(wdist_weight=1, tdist_weight=0, includeMuli=True, includePaused=False, tags=self.current_tags)

    def draw_card(self):
        self.algo.init()
        self.__current_card = self.algo.draw_card()
        return self.__current_card

    @property
    def current_card(self):
        return self.__current_card

    @current_card.setter
    def current_card(self, value):
        self.__current_card = value

    def remove_card(self, card):
        if card == self.__current_card:
            self.current_card = None
        self.session.delete(card)
        self.session.commit()

    def add_card(self, question, answer, context, preamble):
        card = Card(question=question, answer=answer, context=context, paused=False, preamble=preamble)
        self.session.add(card)
        self.session.commit()
        self.refresh_tags()

    def pause_card(self, card):
        card.paused = True
        self.session.commit()