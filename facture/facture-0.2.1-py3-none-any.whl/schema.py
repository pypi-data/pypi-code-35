# -*- coding: utf-8 -*-

from marshmallow import *
from marshmallow import validate


class ParamsSchema(Schema):
    _limit = fields.Integer(missing=100, validate=validate.Range(min=0))
    _offset = fields.Integer(missing=0, validate=validate.Range(min=0))
    _sort = fields.String(missing='')


class CountSchema(Schema):
    count = fields.Integer()


class DeleteSchema(Schema):
    deleted = fields.Integer()
