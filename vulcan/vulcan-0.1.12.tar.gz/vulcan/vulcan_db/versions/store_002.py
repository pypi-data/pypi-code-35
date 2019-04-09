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
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import select
from sqlalchemy.orm import column_property

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, VARCHAR, TEXT, Boolean
import sqlalchemy

_sessions = {}
version = 2

def get_session(db_path = "~/.vulcan/vulcan.db"):
    path = os.path.expanduser(db_path)
    if 'session' in _sessions:
        return _sessions['session']

    db_exists = os.path.exists(path)

    dirname = os.path.dirname(path)
    
    if dirname and not os.path.isdir(dirname):
      os.makedirs(dirname)

    storage_engine = 'sqlite:///{0}'.format(path)

    engine = sqlalchemy.create_engine(storage_engine, echo=False)
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    session = Session()
    _sessions['session'] = session

    if not db_exists:
        v = MigrateVersion(repository_id='vulcan', repository_path='vulcan_db', version=version)
        session.add(v)
        session.commit()

    return session

Base = declarative_base()

class Common(object):
    def as_dict(self):
        obj = {}
        for k,v in self.__dict__.items():
            if k not in ['_sa_instance_state']:
                obj[k] = v if v != "0" else ''
        return obj

class Card(Base, Common):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    question = Column(String, default="")
    answer = Column(String, default="")
    paused = Column(Integer, default=0)
    preamble = Column(String, default="")
    context = Column(String, default="")
    multi = column_property(answer.contains('\n'))

    def __repr__(self):
        return dedent("""
            Q: %s
            A: %s
            Successes: %i
            Wrong: %i
            """) % (self.question, self.answer, self.successes, self.failures)

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

    # another way of handling column_property
    # @hybrid_property
    # def multi(self):
    #     return '\n' in self.answer

    # @multi.expression
    # def multi(cls):
    #     return cls.answer.contains('\n')

    def pop(self):
        if len(self.history):
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
        if len(self.history):
            return datetime.fromtimestamp(self.history[-1].date)
        else:
            return datetime.fromtimestamp(0)

    def compare_answer(self, answer):
        if self.context == 'python':
            try:
                from yapf.yapflib.yapf_api import FormatCode
                return FormatCode(self.answer)[0].strip() == FormatCode(answer)[0].strip()
            except:
                pass
        return self.answer.lower().strip() == answer.lower().strip()

    @staticmethod
    def from_dict(d):
        history = []
        for h in d['history']:
            history.append(History(**h))
        del d['multi']
        d['history'] = history
        card = Card(**d)
        return card


class Cards(object):
    
    @staticmethod
    def tags():
        session = get_session()
        return [x[0] for x in session.query(Card.context).distinct()]


class History(Base, Common):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    success = Column(Integer)
    qid = Column(Integer, ForeignKey('cards.id'))
    card = relationship("Card", back_populates="history")


Card.history = relationship("History", order_by=History.date, back_populates="card", cascade="save-update, merge, delete")


class MigrateVersion(Base):
    __tablename__ = 'migrate_version'
    repository_id = Column(VARCHAR(250), primary_key=True)
    repository_path = Column(TEXT)
    version = Column(Integer)
