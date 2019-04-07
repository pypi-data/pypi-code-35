# -*- coding: utf-8 -*-
import redis
from scrapy import log


class RedisPool():
    __pool = None
    

    def __init__(self, redis_info):
        if RedisPool.__pool is None:
            try:
                RedisPool.__pool = redis.ConnectionPool(host=redis_info["ip"], port=redis_info["port"], password=redis_info["password"], db=redis_info.get('db_index',0))
                log.msg("connecting with redis successfully")
            except Exception as e:
                log.msg("error occured during connecting with redis: %s"%(e))

    @staticmethod
    def __get_redis_connection():
        return redis.StrictRedis(connection_pool=RedisPool.__pool)

    @staticmethod
    def lpush_string(key, str):
        try:
            RedisPool.__get_redis_connection().lpush(key, str)
        except Exception as e:
            log.msg("error occured when lpushing records: %s"%(e))

    @staticmethod
    def insert_string(key, str):
        try:
            RedisPool.__get_redis_connection().set(key,str)
        except Exception as e:
            log.msg("error occured when inserting records: %s"%(e))

    @staticmethod
    def get_value(key):
        try:
            return RedisPool.__get_redis_connection().get(key)
        except Exception as e:
            log.msg("error occured when geting key-values: %s"%(e))
