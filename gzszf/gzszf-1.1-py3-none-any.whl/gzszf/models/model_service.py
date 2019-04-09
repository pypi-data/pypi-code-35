# -*- coding: utf-8 -*-
# @Time : 2019/4/8 11:14
# @Author : Allen
# @Site :
from gzszf.config import db_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import *


class ModelService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
            db_config['user'], db_config['password'], db_config['host'], db_config['port'], db_config['name']))
        self.db_session = sessionmaker(bind=self.engine)
        self.session = self.db_session()

    def close_session(self):
        self.session.close()

    def insert_gzszf_data_guidance(self, data_list):
        self.session.add_all(
            [GzszfDataGuidance(
                area_id=d['area_id'],
                title=d['title'],
                url=d['url'],
                dept=d['dept'],
                create_time=d['create_time'],
                flag=False,
                cat_name=d['cat'],
            )
                for d in data_list]
        )
        self.session.commit()
        self.session.flush()
        return "成功插入 {} ".format(data_list[0]['cat'])
