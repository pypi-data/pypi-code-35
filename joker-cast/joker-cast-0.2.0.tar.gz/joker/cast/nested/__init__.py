#!/user/bin/env python3
# coding: utf-8


def recursive_get(nested_container, *keys):
    for k in keys:
        v = nested_container.get(k)
        if v is None:
            return None
        nested_container = v
    return nested_container


def recursive_sort(structure, key=None):
    from copy import deepcopy
    if isinstance(structure, (list, tuple, set, frozenset)):
        return [recursive_sort(x, key) for x in sorted(structure, key=key)]
    elif isinstance(structure, dict):
        return {k: recursive_sort(v, key) for k, v in structure.items()}
    return deepcopy(structure)
