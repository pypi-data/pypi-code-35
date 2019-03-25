import os
import logging
from functools import partialmethod

from redis import StrictRedis

logger = logging.getLogger(__name__)


class RedisProxy:
    def __init__(self, backend):
        self.backend = backend

    def _decode_response(self, values):
        if isinstance(values, bytes):
            return values.decode("utf-8")

        if isinstance(values, list):
            new_values = []
            for element in values:
                if isinstance(element, bytes):
                    element = element.decode("utf-8")
                new_values.append(element)
            return new_values

        return values

    def proxy(self, method, *args, **kwargs):
        errors = {}

        backend_name = self.backend.__class__.__name__
        try:
            logger.debug(
                "trying to {} {} using {}".format(method, kwargs, backend_name)
            )
            bound_method = getattr(self.backend, method)
            result = bound_method(*args, **kwargs)

            return self._decode_response(result)
        except Exception as e:
            if os.getenv("DEBUG"):
                raise
            errors[backend_name] = str(e)

        raise Exception(
            "No backend managed to {} for the provided request: {}".format(
                method, errors
            )
        )

    lpush = partialmethod(proxy, "lpush")
    lrange = partialmethod(proxy, "lrange")
    erase = partialmethod(proxy, "erase")
    set = partialmethod(proxy, "set")
    get = partialmethod(proxy, "get")
    rpop = partialmethod(proxy, "rpop")
    exists = partialmethod(proxy, "exists")
    hset = partialmethod(proxy, "hset")
    expire = partialmethod(proxy, "expire")
    hmset = partialmethod(proxy, "hmset")
    hmget = partialmethod(proxy, "hmget")
    hdel = partialmethod(proxy, "hdel")


class RedisDummyBackend:
    def __init__(self, **kwargs):
        self.redis_lists = {"set": {}}

    def is_task_new(self, name):
        return name not in self.redis_lists and name not in self.redis_lists["set"]

    def lpush(self, name, elements):
        if not isinstance(elements, list):
            elements = [elements]

        elements = [str(element).encode("utf-8") for element in elements]

        if not name in self.redis_lists:
            self.redis_lists[name] = []

        self.redis_lists[name] = elements + self.redis_lists[name]

    def lrange(self, name, start, end):
        if self.is_task_new(name):
            self.redis_lists[name] = []

        if end == -1:
            return self.redis_lists[name][start:]
        else:
            end = end + 1

        result = self.redis_lists[name][start:end]

        return result

    def erase(self):
        self.redis_lists = {}

    def set(self, name, value, ex=None, nx=None):
        if nx:
            if self.is_task_new(name):
                self.redis_lists["set"][name] = str(value).encode("utf-8")
        else:
            self.redis_lists["set"][name] = str(value).encode("utf-8")

    def get(self, name):
        if not self.is_task_new(name):
            return self.redis_lists["set"][name]

    def rpop(self, name):
        if not self.is_task_new(name):
            if self.redis_lists[name]:
                return self.redis_lists[name].pop(-1)

    def exists(self, name):
        return not self.is_task_new(name)

    def hmset(self, name, mapping):
        if not name in self.redis_lists:
            self.redis_lists[name] = []
        self.redis_lists[name].append(mapping)

    def hmget(self, name, keys):
        if not self.is_task_new(name):
            if self.redis_lists[name]:
                task = self.redis_lists[name][-1]
                task_id = task[keys[0]]
                context = task[keys[1]]
                return task_id, context

    def hdel(self, name, *keys):
        if self.redis_lists[name]:
            self.redis_lists[name].pop(-1)

    def expire(self, name, *args):
        if self.redis_lists[name]:
            del self.redis_lists[name]


def get_backend_configuration():
    return {
        "host": os.getenv("REDIS_HOST") or "localhost",
        "port": os.getenv("REDIS_PORT") or 6379,
        "password": os.getenv("REDIS_PASSWORD") or None,
        "db": os.getenv("REDIS_DB") or "0",
    }


def get_redis_backend(**kwargs):
    def _is_testing():
        return os.getenv("WEB_TESTING") is True or os.getenv("WEB_TESTING") in [
            "True",
            "true",
            "TRUE",
        ]

    if _is_testing():
        return RedisProxy(RedisDummyBackend(**kwargs))

    local_config = get_backend_configuration()
    merged_configuration = {**local_config, **kwargs}

    return RedisProxy(StrictRedis(**merged_configuration))
