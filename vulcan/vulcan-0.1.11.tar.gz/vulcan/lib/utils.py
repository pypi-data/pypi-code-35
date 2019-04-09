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


from vulcan.lib.store import get_session
from vulcan.lib.store import Card
import json
import os

def stats(today=False, total=False):
    session = get_session()
    r = ""
    if today:
        r += f"reviews today: {get_num_cards_studied_today()}"
    if total:
        r += "total cards: {0}".format(session.query(Card).count())
    return r

def get_num_cards_studied_today():
    session = get_session()
    query = session.query(Card)
    n = 0
    for card in query:
        n += card.viewed_today()
    return n

def export(db_path, json_path):
    session = get_session(db_path)
    query = session.query(Card)
    cards = []
    for card in query:
        cards.append(card.as_dict())
    json.dump(cards, open(os.path.expanduser(json_path), 'w'))

def import_to_db(db_path, json_path):
    os.unlink(os.path.expanduser(db_path))
    session = get_session(db_path)
    cards = json.load(open(os.path.expanduser(json_path), 'r'))
    for card in cards:
        c = Card.from_dict(card)
        session.add(c)
    session.commit()


