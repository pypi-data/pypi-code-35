

import json
import unittest

from ..registry import decoders
from ..registry import encoders
from ..serialization import DictConvertible
from ..serialization import JsonEncoder
from ..serialization import JsonerSerializable
from ..serialization import StrConvertible
from ..serialization import json_hook
from ..serialization import maybe_convert_to_obj


class TestStrSerializable(unittest.TestCase):

    def test_000_primitive_type(self):
        self.assertFalse(isinstance(42, JsonerSerializable))

    def test_001_registered_type(self):
        class Dummy:
            pass

        encoders.add(Dummy, 42)
        decoders.add(Dummy, 42)

        self.assertTrue(isinstance(Dummy(), JsonerSerializable))

        del encoders[Dummy]
        del decoders[Dummy]

    def test_002_registered_type(self):
        class Dummy:
            pass

        encoders.add(Dummy, 42)
        decoders.add(Dummy, 42)

        self.assertFalse(isinstance(Dummy, JsonerSerializable))

        del encoders[Dummy]
        del decoders[Dummy]

    def test_003_registered_type(self):
        class Dummy:
            pass

        encoders.add(Dummy, 42)
        decoders.add(Dummy, 42)

        self.assertTrue(issubclass(Dummy, JsonerSerializable))

        del encoders[Dummy]
        del decoders[Dummy]

    def test_004_dict_convertible(self):
        class A:
            def to_dict(self) -> dict:
                return {}

            def from_dict(self, d: dict) -> 'A':
                return A()

        self.assertTrue(isinstance(A(), JsonerSerializable))
        self.assertTrue(issubclass(A, JsonerSerializable))

    def test_005_dict_convertible(self):
        with self.assertRaises(NotImplementedError):
            DictConvertible.from_dict({})
        with self.assertRaises(NotImplementedError):
            DictConvertible.to_dict({})


class TestDictConvertible(unittest.TestCase):
    def test_000_dict_convertible(self):
        class A:
            def to_dict(self) -> dict:
                return {}

            @classmethod
            def from_dict(cls, d: dict) -> 'A':
                return A()

        self.assertTrue(isinstance(A(), DictConvertible))
        self.assertTrue(issubclass(A, DictConvertible))


class TestStrConvertible(unittest.TestCase):
    def test_000_str_convertible(self):
        class A:
            def to_str(self) -> str:
                return ''

            @classmethod
            def from_str(cls, s: str) -> 'A':
                return A()

        self.assertTrue(isinstance(A(), StrConvertible))
        self.assertTrue(issubclass(A, StrConvertible))

    def test_002_str_convertible(self):
        with self.assertRaises(NotImplementedError):
            StrConvertible.from_str('')
        with self.assertRaises(NotImplementedError):
            StrConvertible.to_str('')


class Dummy:
    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Dummy)
        return True


class DummyDictConvertible:
    def to_dict(self) -> dict:
        return {}

    @classmethod
    def from_dict(cls, d: dict) -> 'DummyDictConvertible':
        return cls()


class DummyStrConvertible:
    def to_str(self) -> str:
        return ''

    @classmethod
    def from_str(cls, s: str) -> 'DummyStrConvertible':
        return cls()


class TestJsonEncoder(unittest.TestCase):

    def test_000_default_pass_dict(self):
        encoder = JsonEncoder()

        result = encoder.encode({'foo': 42})
        expected = '{"foo": 42}'

        self.assertEqual(result, expected)

    def test_001_default_pass_int(self):
        encoder = JsonEncoder()

        result = encoder.encode(42)
        expected = '42'

        self.assertEqual(result, expected)

    def test_002_pass_dict_convertible_object(self):
        encoder = JsonEncoder()

        result = encoder.encode(DummyDictConvertible())
        result = json.loads(result)
        expected = '{"__obj_cls__": "jsoner.tests.test_serialization.DummyDictConvertible", ' \
                   '"__json_data__": {}}'
        expected = json.loads(expected)

        self.assertDictEqual(result, expected)

    def test_003_pass_str_convertible_object(self):
        encoder = JsonEncoder()

        result = encoder.encode(DummyStrConvertible())
        result = json.loads(result)
        expected = '{"__obj_cls__": "jsoner.tests.test_serialization.DummyStrConvertible", ' \
                   '"__json_data__": ""}'
        expected = json.loads(expected)

        self.assertDictEqual(result, expected)

    def test_004_in_registry(self):
        encoder = JsonEncoder()

        class A:
            pass

        @encoders.register(A)
        def encode(obj: A) -> str:
            return ''

        @decoders.register(A)
        def decode(data: str) -> A:
            return A()

        result = encoder.encode(A())

        expected = {
            '__obj_cls__': A.__module__ + '.' + A.__qualname__,
            '__json_data__': ''
        }
        self.assertDictEqual(json.loads(result), expected)

        del encoders[A]
        del decoders[A]

    def test_005_in_registry(self):
        encoder = JsonEncoder()

        class A:
            pass

        encoders.add(A, 42)
        decoders.add(A, A())

        result = encoder.encode(A())
        expected = {
            '__obj_cls__': A.__module__ + '.' + A.__qualname__,
            '__json_data__': 42
        }

        self.assertDictEqual(json.loads(result), expected)

        del encoders[A]
        del decoders[A]

    def test_006_encode_cls(self):
        encoder = JsonEncoder()

        encoders.add(Dummy, 42)
        decoders.add(Dummy, Dummy())

        self.assertTrue(issubclass(Dummy, JsonerSerializable))

        result = encoder.encode(Dummy)
        expected = {'__cls__': Dummy.__module__ + '.' + Dummy.__qualname__}
        self.assertDictEqual(json.loads(result), expected)

        del encoders[Dummy]
        del decoders[Dummy]

    def test_007_encode_str(self):
        encoder = JsonEncoder()

        result = encoder.encode('foo')
        expected = "foo"
        self.assertEqual(json.loads(result), expected)

    def test_008_not_in_registry(self):
        encoder = JsonEncoder()

        class Dummy:
            pass

        self.assertRaises(TypeError, encoder.encode, Dummy())


class TestDecoding(unittest.TestCase):
    def test_000_maybe_convert_to_obj(self):
        self.assertDictEqual(maybe_convert_to_obj({}), {})

    def test_001_maybe_convert_to_obj(self):
        data = {
            '__cls__': Dummy.__module__ + '.' + Dummy.__qualname__
        }
        self.assertIs(maybe_convert_to_obj(data), Dummy)

    def test_002_maybe_convert_to_dict(self):
        data = {
            '__obj_cls__': Dummy.__module__ + '.' + Dummy.__qualname__
        }
        decoders.add(Dummy, lambda d: Dummy())

        self.assertEqual(maybe_convert_to_obj(data), Dummy())

        del decoders[Dummy]

    def test_003_object_not_found(self):
        data = {'__cls__': 'abc.abc'}

        self.assertIs(maybe_convert_to_obj(data), data)

    def test_005_object_not_found(self):
        data = {'__obj_cls__': 'abc.abc'}

        self.assertIs(maybe_convert_to_obj(data), data)

    def test_006_str_convertible(self):
        data = {
            "__obj_cls__": "jsoner.tests.test_serialization.DummyStrConvertible",
            "__json_data__": ""
        }

        result = maybe_convert_to_obj(data)

        self.assertIsInstance(result, DummyStrConvertible)

    def test_007_dict_convertible(self):
        data = {
            "__obj_cls__": "jsoner.tests.test_serialization.DummyDictConvertible",
            "__json_data__": {}
        }

        result = maybe_convert_to_obj(data)

        self.assertIsInstance(result, DummyDictConvertible)

    def test_008_not_registered(self):
        data = {
            "__obj_cls__": "jsoner.tests.test_serialization.Dummy",
            "__json_data__": {}
        }

        result = maybe_convert_to_obj(data)

        self.assertDictEqual(result, data)

    def test_009_registered_obj(self):
        data = {
            '__obj_cls__': Dummy.__module__ + '.' + Dummy.__qualname__
        }

        @decoders.register(Dummy)
        def decode(data, cls):
            assert cls is Dummy
            return cls()

        self.assertEqual(maybe_convert_to_obj(data), Dummy())

        del decoders[Dummy]

    def test_010_register_arbitrary_objects(self):
        data = {
            '__obj_cls__': Dummy.__module__ + '.' + Dummy.__qualname__
        }

        decoders.add(Dummy, 42)

        self.assertEqual(maybe_convert_to_obj(data), 42)

        del decoders[Dummy]


class TestJsonHook(unittest.TestCase):
    def test_000_json_hook(self):
        self.assertEqual(json_hook(''), '')

    def test_001_json_hook(self):
        self.assertEqual(json_hook({}), {})

    def test_002_json_hook(self):
        data = {
            "__obj_cls__": "jsoner.tests.test_serialization.Dummy",
            "__json_data__": {}
        }

        result = json_hook(data)

        self.assertDictEqual(result, data)

    def test_003_dict_convertible(self):
        data = {
            "__obj_cls__": "jsoner.tests.test_serialization.DummyDictConvertible",
            "__json_data__": {}
        }

        result = json_hook(data)

        self.assertIsInstance(result, DummyDictConvertible)

    def test_004_str_convertible(self):
        data = {
            "__obj_cls__": "jsoner.tests.test_serialization.DummyStrConvertible",
            "__json_data__": ""
        }

        result = json_hook(data)

        self.assertIsInstance(result, DummyStrConvertible)
