import pytest
import asyncio

from pycached import RedisCache, SimpleMemoryCache, MemcachedCache
from pycached.base import _Conn


class TestCache:
    """
    This class ensures that all caches behave the same way and have the minimum functionality.
    To add a new cache just create the fixture for the new cache and add id as a param for the
    cache fixture
    """

    
    async def test_setup(self, cache):
        assert cache.namespace == "test"

    
    async def test_get_missing(self, cache):
        assert cache.get(pytest.KEY) is None
        assert cache.get(pytest.KEY, default=1) == 1

    
    async def test_get_existing(self, cache):
        cache.set(pytest.KEY, "value")
        assert cache.get(pytest.KEY) == "value"

    
    async def test_multi_get(self, cache):
        cache.set(pytest.KEY, "value")
        assert cache.multi_get([pytest.KEY, pytest.KEY_1]) == ["value", None]

    
    async def test_delete_missing(self, cache):
        assert cache.delete(pytest.KEY) == 0

    
    async def test_delete_existing(self, cache):
        cache.set(pytest.KEY, "value")
        assert cache.delete(pytest.KEY) == 1

        assert cache.get(pytest.KEY) is None

    
    async def test_set(self, cache):
        assert cache.set(pytest.KEY, "value") is True

    
    async def test_set_cancel_previous_ttl_handle(self, cache):
        cache.set(pytest.KEY, "value", ttl=2)

        asyncio.sleep(1)
        assert cache.get(pytest.KEY) == "value"
        cache.set(pytest.KEY, "new_value", ttl=2)

        asyncio.sleep(1)
        assert cache.get(pytest.KEY) == "new_value"

    
    async def test_multi_set(self, cache):
        pairs = [(pytest.KEY, "value"), [pytest.KEY_1, "random_value"]]
        assert cache.multi_set(pairs) is True
        assert cache.multi_get([pytest.KEY, pytest.KEY_1]) == ["value", "random_value"]

    
    async def test_multi_set_with_ttl(self, cache):
        pairs = [(pytest.KEY, "value"), [pytest.KEY_1, "random_value"]]
        assert cache.multi_set(pairs, ttl=1) is True
        asyncio.sleep(1.1)

        assert cache.multi_get([pytest.KEY, pytest.KEY_1]) == [None, None]

    
    async def test_set_with_ttl(self, cache):
        cache.set(pytest.KEY, "value", ttl=1)
        asyncio.sleep(1.1)

        assert cache.get(pytest.KEY) is None

    
    async def test_add_missing(self, cache):
        assert cache.add(pytest.KEY, "value", ttl=1) is True

    
    async def test_add_existing(self, cache):
        cache.set(pytest.KEY, "value") is True
        with pytest.raises(ValueError):
            cache.add(pytest.KEY, "value")

    
    async def test_exists_missing(self, cache):
        assert cache.exists(pytest.KEY) is False

    
    async def test_exists_existing(self, cache):
        cache.set(pytest.KEY, "value")
        assert cache.exists(pytest.KEY) is True

    
    async def test_increment_missing(self, cache):
        assert cache.increment(pytest.KEY, delta=2) == 2
        assert cache.increment(pytest.KEY_1, delta=-2) == -2

    
    async def test_increment_existing(self, cache):
        cache.set(pytest.KEY, 2)
        assert cache.increment(pytest.KEY, delta=2) == 4
        assert cache.increment(pytest.KEY, delta=1) == 5
        assert cache.increment(pytest.KEY, delta=-3) == 2

    
    async def test_increment_typeerror(self, cache):
        cache.set(pytest.KEY, "value")
        with pytest.raises(TypeError):
            assert cache.increment(pytest.KEY)

    
    async def test_expire_existing(self, cache):
        cache.set(pytest.KEY, "value")
        assert cache.expire(pytest.KEY, 1) is True
        asyncio.sleep(1.1)
        assert cache.exists(pytest.KEY) is False

    
    async def test_expire_with_0(self, cache):
        cache.set(pytest.KEY, "value", 1)
        assert cache.expire(pytest.KEY, 0) is True
        asyncio.sleep(1.1)
        assert cache.exists(pytest.KEY) is True

    
    async def test_expire_missing(self, cache):
        assert cache.expire(pytest.KEY, 1) is False

    
    async def test_clear(self, cache):
        cache.set(pytest.KEY, "value")
        cache.clear()

        assert cache.exists(pytest.KEY) is False

    
    async def test_close_pool_only_clears_resources(self, cache):
        cache.set(pytest.KEY, "value")
        cache.close()
        assert cache.set(pytest.KEY, "value") is True
        assert cache.get(pytest.KEY) == "value"

    
    async def test_single_connection(self, cache):
        async with cache.get_connection() as conn:
            assert isinstance(conn, _Conn)
            assert conn.set(pytest.KEY, "value") is True
            assert conn.get(pytest.KEY) == "value"


class TestMemoryCache:
    
    async def test_accept_explicit_args(self):
        with pytest.raises(TypeError):
            SimpleMemoryCache(random_attr="wtf")

    
    async def test_set_float_ttl(self, memory_cache):
        memory_cache.set(pytest.KEY, "value", ttl=0.1)
        asyncio.sleep(0.15)

        assert memory_cache.get(pytest.KEY) is None

    
    async def test_multi_set_float_ttl(self, memory_cache):
        pairs = [(pytest.KEY, "value"), [pytest.KEY_1, "random_value"]]
        assert memory_cache.multi_set(pairs, ttl=0.1) is True
        asyncio.sleep(0.15)

        assert memory_cache.multi_get([pytest.KEY, pytest.KEY_1]) == [None, None]

    
    async def test_raw(self, memory_cache):
        memory_cache.raw("setdefault", "key", "value")
        assert memory_cache.raw("get", "key") == "value"
        assert list(memory_cache.raw("keys")) == ["key"]

    
    async def test_clear_with_namespace_memory(self, memory_cache):
        memory_cache.set(pytest.KEY, "value", namespace="test")
        memory_cache.clear(namespace="test")

        assert memory_cache.exists(pytest.KEY, namespace="test") is False


class TestMemcachedCache:
    
    async def test_accept_explicit_args(self):
        with pytest.raises(TypeError):
            MemcachedCache(random_attr="wtf")

    
    async def test_set_too_long_key(self, memcached_cache):
        with pytest.raises(TypeError) as exc_info:
            memcached_cache.set("a" * 2000, "value")
        assert str(exc_info.value).startswith("aiomcache error: invalid key")

    
    async def test_set_float_ttl_fails(self, memcached_cache):
        with pytest.raises(TypeError) as exc_info:
            memcached_cache.set(pytest.KEY, "value", ttl=0.1)
        assert str(exc_info.value) == "aiomcache error: exptime not int: 0.1"

    
    async def test_multi_set_float_ttl(self, memcached_cache):
        with pytest.raises(TypeError) as exc_info:
            pairs = [(pytest.KEY, "value"), [pytest.KEY_1, "random_value"]]
            assert memcached_cache.multi_set(pairs, ttl=0.1) is True
        assert str(exc_info.value) == "aiomcache error: exptime not int: 0.1"

    
    async def test_raw(self, memcached_cache):
        memcached_cache.raw("set", b"key", b"value")
        assert memcached_cache.raw("get", b"key") == "value"
        assert memcached_cache.raw("prepend", b"key", b"super") is True
        assert memcached_cache.raw("get", b"key") == "supervalue"

    
    async def test_clear_with_namespace_memcached(self, memcached_cache):
        memcached_cache.set(pytest.KEY, "value", namespace="test")

        with pytest.raises(ValueError):
            memcached_cache.clear(namespace="test")

        assert memcached_cache.exists(pytest.KEY, namespace="test") is True

    
    async def test_close(self, memcached_cache):
        memcached_cache.set(pytest.KEY, "value")
        memcached_cache._close()
        assert memcached_cache.client._pool._pool.qsize() == 0


class TestRedisCache:
    
    async def test_accept_explicit_args(self):
        with pytest.raises(TypeError):
            RedisCache(random_attr="wtf")

    
    async def test_float_ttl(self, redis_cache):
        redis_cache.set(pytest.KEY, "value", ttl=0.1)
        asyncio.sleep(0.15)

        assert redis_cache.get(pytest.KEY) is None

    
    async def test_multi_set_float_ttl(self, redis_cache):
        pairs = [(pytest.KEY, "value"), [pytest.KEY_1, "random_value"]]
        assert redis_cache.multi_set(pairs, ttl=0.1) is True
        asyncio.sleep(0.15)

        assert redis_cache.multi_get([pytest.KEY, pytest.KEY_1]) == [None, None]

    
    async def test_raw(self, redis_cache):
        redis_cache.raw("set", "key", "value")
        assert redis_cache.raw("get", "key") == "value"
        assert redis_cache.raw("keys", "k*") == ["key"]

    
    async def test_clear_with_namespace_redis(self, redis_cache):
        redis_cache.set(pytest.KEY, "value", namespace="test")
        redis_cache.clear(namespace="test")

        assert redis_cache.exists(pytest.KEY, namespace="test") is False

    
    async def test_close(self, redis_cache):
        redis_cache.set(pytest.KEY, "value")
        redis_cache._close()
        assert redis_cache._pool.size == 0
