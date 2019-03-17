from collections import defaultdict

from dffr.utils import make_dict_vals_hashable, make_hashable_list, find_diff


def test_make_dict_vals_hashable():
    data = {'a': [1, 2], 'b': {'x': 2}}
    expected = {'a': (1, 2), 'b': (('x', 2),)}
    assert make_dict_vals_hashable(data) == expected


def test_make_hashable_list():
    assert make_hashable_list([1, 2, [3, 4]]) == (1, 2, (3, 4))


def test_find_diff():
    old = {'a': 1}
    new = {'a': 1, 'b': 2}
    assert find_diff(old, new) == defaultdict(list, {'b': [2]})
