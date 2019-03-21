"""Just enough to prove it kind of works."""

import unittest

from . import EZJL, EZJD, as_traversable


class TestEquality(unittest.TestCase):

    """Test some equality."""

    def test_list_traversable(self):
        val = [0, [1]]
        self.assertEqual(EZJL(val), as_traversable(val))

    def test_dict_traversable(self):
        val = {'0': {'1': '2'}}
        self.assertEqual(EZJD(val), as_traversable(val))


class TestListAccess(unittest.TestCase):

    """Test accessing lists."""

    raw = [[0, 1], [2, 3], [4, 5]]
    val = EZJL(raw)

    def test_int(self):
        for i in range(-1, 3):
            self.assertEqual(self.val[i], EZJL(self.raw, path=i))

    def test_int_as_str(self):
        for i in range(-1, 3):
            self.assertEqual(self.val[str(i)], EZJL(self.raw, path=str(i)))

    def test_int_str_mix(self):
        for i in range(-1, 3):
            self.assertEqual(self.val[i], EZJL(self.raw, path=str(i)))
            self.assertEqual(self.val[str(i)], EZJL(self.raw, path=i))

    def test_slice(self):
        cases = {
            '0:3': slice(0, 3),
            ':': slice(None, None),
            '0:1': slice(0, 1)
        }

        for k, v in cases.items():
            self.assertEqual(self.val[k], EZJL(self.raw, path=v))
            self.assertEqual(self.val[k], EZJL(self.raw, path=k))
            self.assertEqual(self.val[v], EZJL(self.raw, path=v))
            self.assertEqual(self.val[v], EZJL(self.raw, path=k))

    def test_simple_nesting(self):
        self.assertEqual(self.val['0.1'], 1)
        self.assertEqual(self.val['1.1'], 3)

    def test_map(self):
        raw = [[[0], [1], [2]]]
        thing = EZJL(raw)
        self.assertEqual(self.val['0:3^.1'], EZJL(self.raw, path='0:3^.1'))
        self.assertEqual(thing['0^.0'], EZJL(raw, path='0^.0'))


class TestDictAccess(unittest.TestCase):

    """Test accessing dicts."""

    raw = {
        'a': {'name': 'Jane', 'age': 12},
        'b': {'name': 'John', 'age': 14},
        'c': {'name': 'Jill', 'age': 10}
    }
    val = EZJD(raw)

    def test_simple(self):
        for key in self.val.keys():
            self.assertEqual(self.val[key], EZJD(self.raw, path=key))

    def test_nested(self):
        self.assertEqual(self.val['a.name'], 'Jane')
        self.assertEqual(self.val['a.age'], 12)

    def test_map(self):
        self.assertEqual(self.val['^.__key'], EZJL(self.raw, path='^.__key'))
        self.assertEqual(self.val['^.name'], EZJL(self.raw, path='^.name'))
        self.assertEqual(self.val['^.age'], EZJL(self.raw, path='^.age'))


class TestProperties(unittest.TestCase):

    """Test properties."""

    dict_ = EZJD({
        'a': {'name': 'Jane', 'age': {'unit': 'year', 'value': 12}},
        'b': {'name': 'John', 'age': {'unit': 'year', 'value': 14}},
        'c': {'name': 'Jill', 'age': {'unit': 'year', 'value': 10}}
    })

    list_ = EZJL([[0, [1, 2]], [1, [2, 3]], [2, [3, 4]]])

    def test_dict_path(self):
        self.assertEqual(self.dict_['b.age'].path, 'b.age')
        self.assertEqual(self.dict_['b.age'].key, 'age')
        self.assertEqual(self.dict_['^.age.value'].path, '^.age.value')
        self.assertEqual(self.dict_['^.age.value'].key, 'value')

    def test_list_path(self):
        self.assertEqual(self.list_['1.1'].path, '1.1')
        self.assertEqual(self.list_['1.1'].key, '1')
        self.assertEqual(self.list_[':^.1.0'].path, ':^.1.0')
        self.assertEqual(self.list_[':^.1.0'].key, '0')

    def test_dict_ancestors(self):
        self.assertEqual(self.dict_['b.age'].parent, self.dict_['b'])
        self.assertEqual(self.dict_['b.age'].root, self.dict_)
        self.assertEqual(self.dict_['^.age.value'].root, self.dict_)

    def test_list_ancestors(self):
        self.assertEqual(self.list_['1.1'].parent, self.list_['1'])
        self.assertEqual(self.list_['1.1'].root, self.list_)
        self.assertEqual(self.list_[':^.1.0'].root, self.list_)


class TestGet(unittest.TestCase):

    """Test exception-safe get method."""

    dict_ = EZJD({
        'a': {'name': 'Jane', 'age': {'unit': 'year', 'value': 12}},
        'b': {'name': 'John', 'age': {'unit': 'year', 'value': 14}},
        'c': {'name': 'Jill', 'age': {'unit': 'year', 'value': 10}}
    })

    list_ = EZJL([[0, [1, 2]], [1, [2, 3]], [2, [3, 4]]])

    def test_dict_exists(self):
        self.assertEqual(self.dict_.get('a.name'), 'Jane')

    def test_dict_not_exists(self):
        self.assertEqual(self.dict_.get('a.gender'), None)
        self.assertEqual(self.dict_.get('a.gender', 'Unknown'), 'Unknown')

    def test_list_exists(self):
        self.assertEqual(self.list_.get('0.1.0'), 1)

    def test_list_not_exists(self):
        self.assertEqual(self.list_.get('0.1.2'), None)
        self.assertEqual(self.list_.get('0.1.2', -1), -1)


class TestString(unittest.TestCase):

    """Test converting strings to traversables."""

    def test_simple_list(self):
        string = '[1, 2, 3]'
        ezjl = EZJL([1, 2, 3])
        self.assertEqual(as_traversable(string), ezjl)

    def test_simple_dict(self):
        string = '{"a": 1, "b": 2, "c": 3}'
        ezjd = EZJD({'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(as_traversable(string), ezjd)

    def test_funky(self):
        string = '{"list": [1, 2, {}], "dict": {"a": ["b", 3]}}'
        traversable = as_traversable({
            'list': [1, 2, {}],
            'dict': {'a': ['b', 3]}
        })
        self.assertEqual(as_traversable(string), traversable)

    def test_ast(self):
        string = "['a', 'b', {'c': 1}]"
        traversable = as_traversable(['a', 'b', {'c': 1}])
        self.assertEqual(as_traversable(string), traversable)


class IteratedAreTraversable(unittest.TestCase):

    """Test iterated objects spew out traversable objects."""

    def test_simple_list(self):
        for obj in EZJL([[1], {'a': 1}, {}]):
            self.assertIsInstance(obj, (EZJL, EZJD))


if __name__ == '__main__':
    unittest.main()
