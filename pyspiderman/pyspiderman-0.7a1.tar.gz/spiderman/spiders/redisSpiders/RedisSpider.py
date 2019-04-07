# -*- coding:utf8 -*-
from scrapy_redis.spiders import RedisSpider
from pydispatch import dispatcher
from scrapy import signals
import re
import time
from spiderman.utils.DB.MysqlPool import MysqlPool
from spiderman.utils.Monitor.StatsMonitor import StatsMonitor
from datetime import datetime
import logging
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class RedisSpider(RedisSpider):
    """Spider that reads urls from redis queue (redisspider:start_urls)."""
    name = 'redis_spider'
    redis_key = 'redis_spider:start_urls'
    allowd_domains = ["blog.jobbole.com"]
    custom_settings = {
        'DUPEFILTER_CLASS' : "scrapy_redis.dupefilter.RFPDupeFilter",  
        'SCHEDULER' : "scrapy_redis.scheduler.Scheduler",
        'SCHEDULER_PERSIST' : True,
        'REDIS_HOST' : "localhost",
        'REDIS_PORT' : "6379",
        # 'REDIS_PARAMS' :{
        #     'password': 'ranbospider',  # 服务器的redis对应密码
        # },
        'DOWNLOADER_MIDDLEWARES' : {
            'spiderman.utils.Monitor.StatsMonitor.StatsMonitor': 543
        },
        'DOWNLOAD_DELAY' : 0.5,
        'LOG_ENABLED' : True,
        'LOG_ENCODING' : 'utf8',
        'LOG_LEVEL' : 'INFO',
    }

    def __init__(self,**kwargs):
        self._kwargs = kwargs
        DB_INFO = {
            "username": "root",
            "password": "admin",
            "host": "127.0.0.1",
            "port": 3306,
            "db": "spiderdb",
        }
        self._db_link = MysqlPool(DB_INFO)
    

    def parse(self, response):
        print(response.css('title::text').extract_first())
                

                