# -*- coding: utf-8 -*-
# Copyright 2019 Mateusz Klos
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
""" Serafin integration with SQLAlchemy. """
from __future__ import absolute_import, unicode_literals

# local imports
from serafin import serialize, util


__version__ = '0.1'


def make_serializer(model_base_class):
    """ Create serialize for the given SQLAlchemy base model class.

    This is the class you get by calling SQLAlchemy's declarative_base()
    """
    @serialize.type(model_base_class)
    def serialize_flask_model(obj, spec, ctx):
        """ serafin serializer for ndb models. """
        if spec is True or spec.empty():
            return {}

        props = list(util.iter_public_props(obj, lambda n, v: n in spec))
        ret = {}

        ret.update(_serialize_flask_model_fields(obj, spec, ctx))
        ret.update({k: serialize.raw(val, spec[k], ctx) for k, val in props})

        return ret

    return serialize_flask_model


def _serialize_flask_model_fields(model, spec, ctx):
    """ Serialize SQLAlchemy model class fields. """
    ret = {}

    columns = model.__table__.columns.items()

    for name, _ in columns:
        if name in spec:
            value = getattr(model, name)
            ret[name] = serialize.raw(value, spec[name], ctx)

    return ret
