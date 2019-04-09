# -*- coding: utf-8 -*- 
# @Time : 2019/4/8 11:14 
# @Author : Allen 
# @Site :

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Integer, DATETIME, Boolean
from uuid import uuid4
from datetime import datetime


class TimeStampCreateUpdate(object):
    update_time = Column(DATETIME, onupdate=datetime.now)


base = declarative_base()


class GzszfDataGuidance(base, TimeStampCreateUpdate):
    __tablename__ = 'gzszf_data_guidance'
    id = Column(Integer, autoincrement=True, primary_key=True)
    area_id = Column(Integer)
    theme_id = Column(Integer)
    title = Column(Text)
    url = Column(String(150))
    dept = Column(String(200))
    create_time = Column(DATETIME)
    update_time = Column(DATETIME)
    flag = Column(Boolean)
    cat_name = Column(String(200))
