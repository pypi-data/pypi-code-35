import pickle

from flask import request
from flask_restful import Resource


class BaseResource(Resource):
    owner = None
    cache = None

    @staticmethod
    def get_args(key, default=None, type=None):
        return request.args.get(key, default=default, type=type)

    def set_cache(self, name, key, value, expire=60 * 60):
        self.cache.hset(name, key, pickle.dumps(value))
        self.cache.expire(name, expire)

    def get_cache(self, name, key):
        result = self.cache.hget(name, key)
        if result:
            return pickle.loads(result)
        return None

    @staticmethod
    def get_token():
        return request.headers.get('Autorization')
