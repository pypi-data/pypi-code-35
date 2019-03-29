#!/usr/bin/python
# coding: utf8

# Copyright 2019 Skiply
# 
from __future__ import unicode_literals


import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from sqlalchemy import Column, Integer


engine = create_engine('mysql+pymysql://smilio_test:1pwd4test@127.0.0.1/smilio')
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

class SkiplyBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=SkiplyBase)
Base.query = db_session.query_property()