# -*- coding: utf-8 -*-

# Copyright (C) 2017 github.com/shyal
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

from __future__ import division
import math
from store import *
from sqlalchemy import and_, or_
import random
import operator
import time

def stats(session):
    query = session.query(Card)
    num = query.count()
    new = query.filter(Card.successes == 0).count()
    paused = query.filter(Card.paused == True).count()
    young = query.filter(and_(Card.paused == False, Card.successes <= 7)).count()
    mid = query.filter(and_(Card.paused == False, Card.successes > 7, Card.successes <= 9)).count()
    mature = query.filter(and_(Card.paused == False, Card.successes > 9)).count()
    return "Cards: {0}\nNew: {1}\nPaused: {2}\nYoung: {3}\nMid: {4}\nMature: {5}".format(num, new, paused, young, mid, mature)

def weighted_pick(d):
    r = random.uniform(0, sum(d.itervalues()))
    s = 0.0
    for k, w in d.iteritems():
        s += w
        if r < s: return k
    return k

def simple_norm(D):
    newd = {}
    S = sum(D.values())
    N = len(D.keys())
    if S == 0:
        for c in D.keys():
            newd[c] = float(1)/N
    else:
        for c in D.keys():
            newd[c] = float(D[c])/S
    return newd

def get_telapsed(last_draw_timestamp):
    telapsed = {}
    now = datetime.now()
    for card_id, tstamp in last_draw_timestamp.items():
        telapsed[card_id] = (now - tstamp).seconds
    return telapsed

def get_expectation_of_recall(tdist, strength):
    E_recall = {}
    for card_id in tdist.keys():
        t = tdist[card_id]
        s = strength[card_id]
        E_recall[card_id] = math.exp(-t/s)
    return E_recall

def weighted_combination(weights, distributions):
    sum_weights = sum(weights)
    newd = {}
    ndist = len(distributions)
    for card_id in distributions[0]:
        weighted_sum = 0
        for i in range(ndist):
            weighted_sum += (weights[i] * distributions[i][card_id])
        newd[card_id] = weighted_sum / sum_weights
    return newd

def laplace_smoothing_dist(ncards_drawn, card_count):
    dist = {}
    nwords = len(card_count)
    for card_id in card_count:
        dist[card_id] = (float(card_count[card_id]) + 1)/ (ncards_drawn + nwords)
    dist = simple_norm(dist)
    return dist

class FlashcardAlgorithm():
    def __init__(self, wdist_weight=1, tdist_weight=0, includeMuli=1, includePaused=0, tags=[]):
        self.session = get_session()
        self.tags = tags
        self.wdist_weight = wdist_weight
        self.tdist_weight = tdist_weight
        self.includePaused = includePaused
        self.includeMuli = includeMuli
        self.init()

    def init(self):
        filt = and_(or_(Card.paused == 0, Card.paused == self.includePaused), or_(Card.multi == 0, Card.multi == self.includeMuli))
        self.learning_rate = 100
        self.draw_dist = {}
        self.strength = {}
        self.weakness = {}
        self.last_draw_timestamp = {}
        self.unknown_count = {}
        self.known_count = {}
        self.ncards_drawn = 0
        if self.tags:
            filt = and_(filt, Card.context.in_(self.tags))
        for card in self.session.query(Card).filter(filt):
            self.ncards_drawn += card.attempts
            self.known_count[card.id] = card.successes
            self.unknown_count[card.id] = card.failures
            self.last_draw_timestamp[card.id] = card.last_draw_timestamp
        self.strength = laplace_smoothing_dist(self.ncards_drawn, self.known_count)
        self.weakness = laplace_smoothing_dist(self.ncards_drawn, self.unknown_count)

    def get_tdist(self):
        telapsed = get_telapsed(self.last_draw_timestamp)
        tdist = simple_norm(telapsed)
        return tdist

    def show_scores(self, _id = None):
        tdist = self.get_tdist()
        E_recall = get_expectation_of_recall(tdist, self.strength)
        if _id:
            return E_recall[_id]
        else:
            return sorted(E_recall.items(), key=operator.itemgetter(1))

    def show_strength(self, _id=None):
        if _id:
            return self.strength[_id]
        else:
            return sorted(self.strength.items(), key=operator.itemgetter(1), reverse=True)

    def draw_card(self):
        tdist = self.get_tdist()
        E_recall = get_expectation_of_recall(tdist, self.strength)
        self.draw_dist = weighted_combination([self.wdist_weight, self.tdist_weight], [self.weakness, tdist])
        sorted_cards = sorted(E_recall.items(), key=operator.itemgetter(1))
        if sorted_cards:
            card_id = sorted_cards[0][0]
            self.last_draw_timestamp[card_id] = datetime.now()
            self.ncards_drawn += 1
            return self.session.query(Card).filter(Card.id == card_id).first()

    def reply(self, card_id, correct, given_answer, wrong_cb):
        card = self.session.query(Card).filter(Card.id == card_id).first()
        now = int(time.time())
        if correct:
            self.known_count[card_id] += 1
        else:
            self.unknown_count[card_id] += 1
            if wrong_cb:
                wrong_cb(given_answer=given_answer, right_answer=str(card.answer))
        card.history.append(History(success=correct, date=now))
        self.session.commit()
        return True
