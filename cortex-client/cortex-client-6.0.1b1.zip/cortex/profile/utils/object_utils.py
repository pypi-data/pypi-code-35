import uuid
from typing import List, Optional, Any, Tuple

import pandas as pd

__all__ = [
    'unique_id',
    'head',
    'tuples_with_nans_to_tuples_with_nones',
    'split_list_of_tuples',
]

def unique_id() -> str:
    """
    Returns a unique id.
    """
    return str(uuid.uuid4())


def head(l:List[Any]) -> Optional[Any]:
    list_with_first_elem = l[0:1]
    return list_with_first_elem[0] if list_with_first_elem else None


def tuples_with_nans_to_tuples_with_nones(iter:List[Any]) -> Tuple[Any]:
    # - [x] TODO: Dont like the instance check here ... python has no way of saying "isPrimitive"
        # ... I only want to check for NaNs on primitives... and replace them with None ... not Lists ...
        # Realization: NaNs are floats ...!
    return (
        tuple(map(lambda x: None if isinstance(x, float) and pd.isna(x) else x, list(tup)))
        for tup in iter
    )

def split_list_of_tuples(l:List[Tuple[Any,Any]]) -> Tuple[List[Any], List[Any]] :
    """
    NOTE: No python way of specifying that the return type ... the number of List[Any] in it depends on the size of the tuple passed in ...
    :param l:
    :return:
    """
    if not l:
        return l
    lengths_of_each_tuple = map(lambda x: len(list(x)), l)
    all_tuples_same_length =  all(lambda x: x == lengths_of_each_tuple[0], lengths_of_each_tuple)
    assert all_tuples_same_length, "All tuples must be of the same length: {}".format(lengths_of_each_tuple[0])
    return tuple(*[[tupe[i] for tupe in l] for i in range(0, lengths_of_each_tuple[0])])
