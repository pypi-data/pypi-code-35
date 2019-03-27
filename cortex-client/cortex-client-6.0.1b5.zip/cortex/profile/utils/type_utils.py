"""
Copyright 2019 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import typing
from typing import Union, TypeVar, Tuple

NoneType = type(None)
T = TypeVar('T')

__all__ = [
    'is_typing_type',
    'get_types_of_union',
    'is_optional_type',
    'is_union_type',
]

def is_typing_type(t:type) -> bool:
    """
    Is a type from the typing library ...
    Confirmed true for the following typing types:
        - typing.Mapping
        - typing.Tuple
        - typing.Callable
        - typing.Type
        - typing.List
        - typing.Dict
        - typing.DefaultDict
        - typing.Set
        - typing.FrozenSet
        - typing.Counter
        - typing.Deque
    :param t:
    :return:
    """
    return isinstance(t, typing._GenericAlias) or (
        hasattr(t, "__origin__") and t.__origin__ in [typing.Optional, typing.Union]
    )


def get_types_of_union(union:Union) -> Tuple[type]:
    """
    Gets all of the types associated with the union type ...
    :param union:
    :return:
    """
    return tuple(union.__args__)


def is_optional_type(t:type) -> bool:
    """
    Determines if a type is an Option Type ...
    :param t:
    :return:
    """
    # return is_typing_type(t) and len(t.__args__) == 2 and type(None) in t.__args__
    # return t.__origin__ in [typing.Optional]
    return repr(t).startswith('typing.Optional')


def is_union_type(t:type) -> bool:
    """
    Determines if a type is a Union Type ...
    :param t:
    :return:
    """
    # return t.__origin__ in [typing.Union]
    return repr(t).startswith('typing.Union')
