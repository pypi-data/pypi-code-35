# -*- coding: utf-8 -*-
# Copyright 2016-2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
**serafin** is a serialization system that allows flexible serialization
of any type of object according to a provided field spec. The field spec tells
the serialize which attribute/fields/members of the given object should be
serialized. This allows for a very flexible serialization system, especially in
the context of API endpoints where we can write one endpoint and allow client
to pass the field spec describing how he wants the output to be formatted.
"""
from __future__ import absolute_import, unicode_literals
from .context import Context
from .fieldspec import Fieldspec
from .serializer import serialize
from .serializers import *     # pylint: disable=wildcard-import
__version__ = '0.12.2'


__all__ = [
    'Context',
    'Fieldspec',
    'serialize',
]
