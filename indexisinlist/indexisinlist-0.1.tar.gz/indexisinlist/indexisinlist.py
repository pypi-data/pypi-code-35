#!/usr/bin/env python3

from typing import Union, List, Tuple


def index_is_in_list(ls: Union[List, Tuple], index: int) -> bool:
    """
    This function check if an index is in the specified list.

    :param ls: Union[List: Tuple]: List to check.
    :param index: int: Index to check.
    """
    return (0 <= index < len(ls)) or (-len(ls) <= index < 0)
