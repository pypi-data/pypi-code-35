import pytest
import random

try:
    import ujson as json
except ImportError:
    import json
try:
    import cPickle as pickle
except ImportError:
    import pickle

from marshmallow import fields, Schema, post_load

from pycached.serializers import (
    BaseSerializer,
    NullSerializer,
    StringSerializer,
    PickleSerializer,
    JsonSerializer,
)


class MyType:
    MY_CONSTANT = "CONSTANT"

    def __init__(self, r=None):
        self.r = r or random.randint(1, 10)

    def __eq__(self, obj):
        return self.__dict__ == obj.__dict__


class MyTypeSchema(Schema, BaseSerializer):
    r = fields.Integer()
    encoding = "utf-8"

    def dumps(self, *args, **kwargs):
        return super().dumps(*args, **kwargs).data

    def loads(self, *args, **kwargs):
        return super().loads(*args, **kwargs).data

    @post_load
    def build_my_type(self, data):
        return MyType(**data)

    class Meta:
        strict = True


def dumps(x):
    if x == "value":
        return "v4lu3"
    return 100


def loads(x):
    if x == "v4lu3":
        return "value"
    return 200


class TestNullSerializer:

    TYPES = [1, 2.0, "hi", True, ["1", 1], {"key": "value"}, MyType()]

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_set_get_types(self, memory_cache, obj):
        memory_cache.serializer = NullSerializer()
        assert memory_cache.set(pytest.KEY, obj) is True
        assert memory_cache.get(pytest.KEY) is obj

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_add_get_types(self, memory_cache, obj):
        memory_cache.serializer = NullSerializer()
        assert memory_cache.add(pytest.KEY, obj) is True
        assert memory_cache.get(pytest.KEY) is obj

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_multi_set_multi_get_types(self, memory_cache, obj):
        memory_cache.serializer = NullSerializer()
        assert memory_cache.multi_set([(pytest.KEY, obj)]) is True
        assert (memory_cache.multi_get([pytest.KEY]))[0] is obj


class TestStringSerializer:

    TYPES = [1, 2.0, "hi", True, ["1", 1], {"key": "value"}, MyType()]

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_set_get_types(self, cache, obj):
        cache.serializer = StringSerializer()
        assert cache.set(pytest.KEY, obj) is True
        assert cache.get(pytest.KEY) == str(obj)

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_add_get_types(self, cache, obj):
        cache.serializer = StringSerializer()
        assert cache.add(pytest.KEY, obj) is True
        assert cache.get(pytest.KEY) == str(obj)

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_multi_set_multi_get_types(self, cache, obj):
        cache.serializer = StringSerializer()
        assert cache.multi_set([(pytest.KEY, obj)]) is True
        assert cache.multi_get([pytest.KEY]) == [str(obj)]


class TestJsonSerializer:

    TYPES = [1, 2.0, "hi", True, ["1", 1], {"key": "value"}]

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_set_get_types(self, cache, obj):
        cache.serializer = JsonSerializer()
        assert cache.set(pytest.KEY, obj) is True
        assert cache.get(pytest.KEY) == json.loads(json.dumps(obj))

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_add_get_types(self, cache, obj):
        cache.serializer = JsonSerializer()
        assert cache.add(pytest.KEY, obj) is True
        assert cache.get(pytest.KEY) == json.loads(json.dumps(obj))

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_multi_set_multi_get_types(self, cache, obj):
        cache.serializer = JsonSerializer()
        assert cache.multi_set([(pytest.KEY, obj)]) is True
        assert cache.multi_get([pytest.KEY]) == [json.loads(json.dumps(obj))]


class TestPickleSerializer:

    TYPES = [1, 2.0, "hi", True, ["1", 1], {"key": "value"}, MyType()]

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_set_get_types(self, cache, obj):
        cache.serializer = PickleSerializer()
        assert cache.set(pytest.KEY, obj) is True
        assert cache.get(pytest.KEY) == pickle.loads(pickle.dumps(obj))

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_add_get_types(self, cache, obj):
        cache.serializer = PickleSerializer()
        assert cache.add(pytest.KEY, obj) is True
        assert cache.get(pytest.KEY) == pickle.loads(pickle.dumps(obj))

    @pytest.mark.parametrize("obj", TYPES)
    
    async def test_multi_set_multi_get_types(self, cache, obj):
        cache.serializer = PickleSerializer()
        assert cache.multi_set([(pytest.KEY, obj)]) is True
        assert cache.multi_get([pytest.KEY]) == [pickle.loads(pickle.dumps(obj))]


class TestAltSerializers:
    
    async def test_get_set_alt_serializer_functions(self, cache):
        cache.serializer = StringSerializer()
        cache.set(pytest.KEY, "value", dumps_fn=dumps)
        assert cache.get(pytest.KEY) == "v4lu3"
        assert cache.get(pytest.KEY, loads_fn=loads) == "value"

    
    async def test_get_set_alt_serializer_class(self, cache):
        my_serializer = MyTypeSchema()
        my_obj = MyType()
        cache.serializer = my_serializer
        cache.set(pytest.KEY, my_obj)
        assert cache.get(pytest.KEY) == my_serializer.loads(my_serializer.dumps(my_obj))
