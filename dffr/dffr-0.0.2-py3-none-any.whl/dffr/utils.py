from collections import defaultdict


def make_hashable_list(lst: list) -> tuple:
    """
    Recursively converts lists to tuples.

    >>> make_hashable_list([1, [2, [3, [4]]]])
    (1, (2, (3, (4,))))

    """

    for n, index in enumerate(lst):
        if isinstance(index, list):
            lst[n] = make_hashable_list(index)

    return tuple(lst)


def make_dict_vals_hashable(dct: dict) -> dict:
    """
    Recursively converts values of a dict (a type list to a tuple).

    >>> make_dict_vals_hashable({'a': [1, [2]], 'b': {'x': [1, [2]]}})
    {'a': (1, (2,)), 'b': (('x', (1, (2,))),)}

    """

    for k, v in dct.items():
        if isinstance(v, list):
            dct[k] = make_hashable_list(v)
        elif isinstance(v, dict):
            dct[k] = tuple(make_dict_vals_hashable(dct[k]).items())

    return dct


def find_diff(old: dict, new: dict) -> defaultdict:
    """
    Find a difference between two dicts.

    >>> find_diff({'a': 1, 'b': 2}, {'a': 1, 'b': 2, 'c': 3})
    defaultdict(<class 'list'>, {'c': [3]})

    """

    diff_mapping = defaultdict(list)

    old_hashable = make_dict_vals_hashable(old)
    new_hashable = make_dict_vals_hashable(new)

    diff = set(old_hashable.items()) ^ set(new_hashable.items())

    for k, v in diff:
        diff_mapping[k].append(v)

    return diff_mapping
