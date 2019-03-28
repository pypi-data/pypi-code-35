#!-*- coding:utf-8 -*-

import re
import uuid
import time
import redis
import pickle
import random
from datetime import date, datetime, timedelta


class KmuxRedisClient(object):
    __connection_pool_cache__ = dict()

    def __init__(self, host='localhost', port=6379, password=None, database=0, current_time=None):
        if isinstance(host, str):
            if '://' in host:
                conn_pool = KmuxRedisClient.create_conn_pool_from_url(host)
            else:
                conn_pool = KmuxRedisClient.create_conn_pool(host, port, password, database)
        else:
            assert isinstance(host, redis.ConnectionPool)
            conn_pool = host
        self._redis_db = redis.Redis(connection_pool=conn_pool)
        self._current_time = None

        self.current_time = current_time

    @classmethod
    def create_conn_pool_from_url(cls, url):
        cache_id = url
        if cache_id in cls.__connection_pool_cache__:
            conn_pool = cls.__connection_pool_cache__[cache_id]
        else:
            conn_pool = redis.BlockingConnectionPool.from_url(url)
            cls.__connection_pool_cache__.setdefault(cache_id, conn_pool)
        return conn_pool

    @classmethod
    def create_conn_pool(cls, host='localhost', port=6379, password=None, database=0):
        if password:
            url = 'redis://{}@{}:{}/{}'.format(password, host, port, database)
        else:
            url = 'redis://{}:{}/{}'.format(host, port, database)
        return cls.create_conn_pool_from_url(url)

    @property
    def redis_db(self):
        return self._redis_db  # type: redis.Redis

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, v):
        self._current_time = v if isinstance(v, datetime) else datetime.now()

    @staticmethod
    def encode_k(k):
        assert isinstance(k, str)
        return str(k)  # type: str

    @staticmethod
    def decode_k(k):
        assert isinstance(k, str)
        return k  # type: str

    @staticmethod
    def encode_v(v):
        return pickle.dumps(v)  # type: str

    @staticmethod
    def decode_v(v):
        return v if v is None else pickle.loads(v)  # type: object | None

    def ttl(self, name):
        name = self.encode_k(name)
        return self.redis_db.ttl(name)

    def pttl(self, name):
        name = self.encode_k(name)
        return self.redis_db.pttl(name)

    def expire(self, name, ttl, at_least=True):
        name = self.encode_k(name)

        ttl_old = self.redis_db.ttl(name)

        if callable(ttl):
            ttl = ttl()

        if isinstance(ttl, date):
            ttl_new = ttl if isinstance(ttl, datetime) else datetime(year=ttl.year, month=ttl.month, day=ttl.day)
            self.redis_db.expireat(name, ttl_new)
        else:
            if isinstance(ttl, timedelta):
                ttl_new = int(ttl.total_seconds())
            elif isinstance(ttl, (int, float)):
                ttl_new = int(ttl)
            else:
                ttl_new = ttl_old

            ttl_new = max(ttl_new, ttl_old) if at_least else ttl_new

            self.redis_db.expire(name, ttl_new)

    def exists(self, name):
        name = self.encode_k(name)
        return self.redis_db.exists(name)

    def setnx(self, name, value):
        name = self.encode_k(name)
        value = self.encode_v(value)
        return self.redis_db.setnx(name, value)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        name = self.encode_k(name)
        value = self.encode_v(value)
        return self.redis_db.set(name, value, ex, px, nx, xx)

    def get(self, name, default=None):
        name = self.encode_k(name)
        value = default
        if self.redis_db.exists(name):
            value = self.redis_db.get(name)
            value = self.decode_v(value)
        return value

    def delete(self, name):
        name = self.encode_k(name)
        return self.redis_db.delete(name)

    def hexists(self, name, key):
        name = self.encode_k(name)
        key = self.encode_k(key)
        return self.redis_db.hexists(name, key)

    def hsetnx(self, name, key, value):
        name = self.encode_k(name)
        key = self.encode_k(key)
        value = self.encode_v(value)
        return self.redis_db.hsetnx(name, key, value)

    def hset(self, name, key, value):
        name = self.encode_k(name)
        key = self.encode_k(key)
        value = self.encode_v(value)
        return self.redis_db.hset(name, key, value)

    def hget(self, name, key):
        name = self.encode_k(name)
        key = self.encode_k(key)
        value = self.redis_db.hget(name, key)
        value = self.decode_v(value)
        return value

    def sadd(self, name, value):
        name = self.encode_k(name)
        value = self.encode_v(value)
        return self.redis_db.sadd(name, value)

    def srem(self, name, value):
        name = self.encode_k(name)
        value = self.encode_v(value)
        return self.redis_db.srem(name, value)

    def smembers(self, name):
        name = self.encode_k(name)
        values = self.redis_db.smembers(name)
        values = list(values)
        for i in range(len(values)):
            values[i] = self.decode_v(values[i])
        return values

    def scard(self, name):
        name = self.encode_k(name)
        count = self.redis_db.scard(name)
        return count

    def hdel(self, name, key):
        name = self.encode_k(name)
        key = self.encode_k(key)
        return self.redis_db.hdel(name, key)

    def keys(self, pattern, re_pattern=None):
        assert isinstance(pattern, str)
        keys = self.redis_db.keys(pattern)
        if re_pattern is not None:
            assert isinstance(re_pattern, (re.Pattern, str))
            keys, keys_t = [], keys
            if isinstance(re_pattern, str):
                re_pattern = re.compile(re_pattern)
            for k in keys_t:
                if re_pattern.match(k):
                    keys.append(k)
        return keys

    def hgetall(self, name):
        d = dict()
        hd = self.redis_db.hgetall(name)
        if isinstance(hd, dict):
            for (k, v) in hd.items():
                k = self.decode_k(k)
                v = self.decode_v(v)
                d[k] = v
        return d

    def register_script(self, script):
        return self.redis_db.register_script(script)

    def pipeline(self, transaction=True, shard_hint=None):
        return self.redis_db.pipeline(transaction, shard_hint)

    def blpop(self, keys, timeout=0):
        return self.redis_db.blpop(keys, timeout)

    def brpop(self, keys, timeout=0):
        return self.redis_db.brpop(keys, timeout)

    def brpoplpush(self, src, dst, timeout=0):
        return self.redis_db.brpoplpush(src, dst, timeout)

    def lindex(self, name, index):
        return self.redis_db.lindex(name, index)

    def linsert(self, name, where, refvalue, value):
        return self.redis_db.linsert(name, where, refvalue, value)

    def llen(self, name):
        return self.redis_db.llen(name)

    def lpop(self, name):
        return self.redis_db.lpop(name)

    def lpush(self, name, *values):
        return self.redis_db.lpush(name, *values)

    def lpushx(self, name, value):
        return self.redis_db.lpushx(name, value)

    def lrange(self, name, start, end):
        return self.redis_db.lrange(name, start, end)

    def lrem(self, name, count, value):
        return self.redis_db.lrem(name, count, value)

    def lset(self, name, index, value):
        return self.redis_db.lset(name, index, value)

    def ltrim(self, name, start, end):
        return self.redis_db.ltrim(name, start, end)

    def rpop(self, name):
        return self.redis_db.rpop(name)

    def rpoplpush(self, src, dst):
        return self.redis_db.rpoplpush(src, dst)

    def rpush(self, name, *values):
        return self.redis_db.rpush(name, *values)

    def rpushx(self, name, value):
        return self.redis_db.rpushx(name, value)

    def sort(self, name, start=None, num=None, by=None, get=None, desc=False, alpha=False, store=None, groups=False):
        return self.redis_db.sort(name, start, num, by, get, desc, alpha, store, groups)


class KmuxRedisLockError(Exception):
    pass


class KmuxRedisLock(object):
    DEFAULT_RETRY_TIMES = 3
    DEFAULT_RETRY_DELAY = 200
    DEFAULT_TTL = 100000
    CLOCK_DRIFT_FACTOR = 0.01
    RELEASE_LUA_SCRIPT = """
        if redis.call("get",KEYS[1]) == ARGV[1] then
            return redis.call("del",KEYS[1])
        else
            return 0
        end
    """

    def __init__(self, resource, redis_client, retry_times=DEFAULT_RETRY_TIMES, retry_delay=DEFAULT_RETRY_DELAY,
                 ttl=DEFAULT_TTL):
        assert isinstance(redis_client, KmuxRedisClient)
        self._resource = resource
        self._redis_client = redis_client
        self._retry_times = retry_times
        self._retry_delay = retry_delay
        self._ttl = ttl
        self._lock_key = None
        self._redis_client = None

    @property
    def resource(self):
        return self._resource

    @property
    def redis_client(self):
        return self._redis_client

    @property
    def retry_times(self):
        return self._retry_times

    @property
    def retry_delay(self):
        return self._retry_delay

    @property
    def ttl(self):
        return self._ttl

    @property
    def lock_key(self):
        return self._lock_key

    @lock_key.setter
    def lock_key(self, v):
        self._lock_key = v

    def __enter__(self):
        if not self.acquire():
            raise KmuxRedisLockError(u'Failed to acquire RedisLock')

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def _total_ms(self, delta):
        delta_seconds = delta.seconds + delta.days * 24 * 3600
        return (delta.microseconds + delta_seconds * 10 ** 6) / 10 ** 3

    def acquire(self):
        is_acquired = False

        self._lock_key = 'Locks:{}'.format(uuid.uuid4())

        for retry in range(self.retry_times):
            start_time = datetime.utcnow()

            if self._redis_client.set(self.resource, self.lock_key, nx=True, px=self.ttl):
                is_acquired = True

            end_time = datetime.utcnow()
            elapsed_milliseconds = self._total_ms(end_time - start_time)

            drift = (self.ttl * KmuxRedisLock.CLOCK_DRIFT_FACTOR) + 2

            if is_acquired and self.ttl > (elapsed_milliseconds + drift):
                break
            else:
                self.release()
                time.sleep(random.randint(0, self.retry_delay) / 1000)
        return is_acquired

    def release(self):
        if not getattr(self._redis_client, '_release_script', default=None):
            self._redis_client._release_script = self._redis_client.register_script(KmuxRedisLock.RELEASE_LUA_SCRIPT)
        self._redis_client._release_script(keys=[self.resource], args=[self.lock_key])


class KmuxReentrantKmuxRedisLock(KmuxRedisLock):
    def __init__(self, *args, **kwargs):
        super(KmuxReentrantKmuxRedisLock, self).__init__(*args, **kwargs)
        self._acquired_count = 0

    @property
    def acquired_count(self):
        return self._acquired_count

    def acquire(self):
        is_acquired = True
        if self._acquired_count == 0:
            is_acquired = super(KmuxReentrantKmuxRedisLock, self).acquire()

        if is_acquired:
            self._acquired_count += 1

        return is_acquired

    def release(self):
        is_released = False

        if self._acquired_count > 0:
            self._acquired_count -= 1
            if self._acquired_count == 0:
                super(KmuxReentrantKmuxRedisLock, self).release()
                is_released = True

        return is_released

    def release_all(self):
        if self._acquired_count > 0:
            super(KmuxReentrantKmuxRedisLock, self).release()
        self._acquired_count = 0


class KmuxRedisVariable(object):
    def __init__(self, name, redis_client):
        assert isinstance(name, str)
        assert isinstance(redis_client, KmuxRedisClient)
        self._name = name
        self._redis_name = 'vars:{}'.format(name)
        self._redis_client = redis_client
        self._lock = KmuxReentrantKmuxRedisLock(resource=name, redis_client=redis_client)

    @property
    def name(self):
        return self._name

    @property
    def redis_name(self):
        return self._redis_name

    @property
    def redis_client(self):
        return self._redis_client

    @property
    def lock(self):
        return self._lock

    def get_value(self, default=None):
        with self.lock:
            v = self.redis_client.get(self.redis_name, default=default)
        return v

    def set_value(self, v, ttl=None, at_least=False):
        with self.lock:
            self.redis_client.set(self.redis_name, v)
            self.redis_client.expire(self, ttl=ttl, at_least=at_least)

    def expire(self, ttl, at_least=False):
        with self.lock:
            self.redis_client.expire(self, ttl=ttl, at_least=at_least)


class KmuxRedisInt(KmuxRedisVariable):
    def __int__(self):
        return int(self.get_value(0))

    def __add__(self, other):
        with self.lock:
            v = int(self.get_value(0))
            v += other
        return v

    def __iadd__(self, other):
        return self.inc_and_return(other)

    def inc_and_return(self, increment=1):
        with self.lock:
            v = int(self.get_value(0))
            v += increment
            self.set_value(v)
        return v

    def return_and_inc(self, increment=1):
        with self.lock:
            v = int(self.get_value(0))
            vv = v + increment
            self.set_value(vv)
        return v
