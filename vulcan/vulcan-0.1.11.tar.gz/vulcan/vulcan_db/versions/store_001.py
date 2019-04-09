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

import os
from datetime import datetime
from textwrap import dedent
import arrow
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, VARCHAR, TEXT
import sqlalchemy

_sessions = {}

def get_session(db_path = "~/.vulcan/vulcan.db"):
    path = os.path.expanduser(db_path)
    if 'session' in _sessions:
        return _sessions['session']

    dirname = os.path.dirname(path)
    
    if dirname and not os.path.isdir(dirname):
      os.makedirs(dirname)

    storage_engine = 'sqlite:///{0}'.format(path)

    engine = sqlalchemy.create_engine(storage_engine, echo=False)
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    session = Session()
    _sessions['session'] = session
    return session

Base = declarative_base()

class Common(object):
    def as_dict(self):
        obj = {}
        for k,v in self.__dict__.iteritems():
            if k not in ['_sa_instance_state']:
                obj[k] = v if v != "0" else ''
        return obj

class Card(Base, Common):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    question = Column(String, default="")
    answer = Column(String, default="")
    last_answered = Column(Integer, default=0)
    paused = Column(sqlalchemy.types.Boolean, default=False)
    multi = Column(sqlalchemy.types.Boolean, default=False)
    preamble = Column(String, default="")
    closing = Column(String, default="")
    context = Column(String, default="")
    times_asked = Column(Integer, default=0)
    num_successes = Column(Integer, default=0)

    def __repr__(self):
        return dedent("""
            Q: %s
            A: %s
            Successes: %i
            Wrong: %i
            multi: %i
            """) % (self.question, self.answer, self.successes, self.failures, self.multi)

    def print_stats(self, stdout):
        stdout.write("\nSuccesses: %i\nWrong: %i\n"% (self.successes, self.failures))
        stdout.flush()

    @property
    def successes(self):
        return len(list(filter(lambda x: x.success, self.history)))

    @property
    def failures(self):
        return len(list(filter(lambda x: not x.success, self.history)))

    @property
    def attempts(self):
        return len(self.history)

    def pop(self):
        if len(self.history):
            self.num_successes += -self.history[-1]
            self.times_asked -= 1
            self.history = self.history[:-2]

    def as_dict(self):
        card_dict = super(Card, self).as_dict()
        card_dict["history"] = [x.as_dict() for x in self.history]
        return card_dict

    def viewed_today(self):
        for h in self.history:
            if arrow.get(h.date).date() == datetime.now().date():
                return True
        return False

    @property
    def last_draw_timestamp(self):
        return datetime.fromtimestamp(self.last_answered)

    def compare_answer(self, answer):
        if self.context == 'python':
            try:
                from yapf.yapflib.yapf_api import FormatCode
                return FormatCode(self.answer)[0].strip() == FormatCode(answer)[0].strip()
            except:
                pass
        return self.answer.lower().strip() == answer.lower().strip()

class Cards(object):
    
    @staticmethod
    def tags():
        session = get_session()
        return [x[0] for x in session.query(Card.context).distinct()]


class History(Base, Common):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    success = Column(sqlalchemy.types.Boolean)
    qid = Column(Integer, ForeignKey('cards.id'))
    card = relationship("Card", back_populates="history")


Card.history = relationship("History", order_by=History.date, back_populates="card", cascade="save-update, merge, delete")
