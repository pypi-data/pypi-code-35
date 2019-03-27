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

from typing import Callable, Any, Tuple

__all__ = [
    'pass_through_converter',
]


def pass_through_converter(types_that_need_conversion:Tuple, converter_method:Callable) -> Callable[[Any], Any]:
    """
    Returns a method that when invoked with the values, determines whether or not the value should be converted.
    Items that don't need conversion are passed through as is ...

    :param types_that_need_conversion:
    :param converter_method:
    :return:
    """
    return lambda x: converter_method(x) if isinstance(x, types_that_need_conversion) else x
