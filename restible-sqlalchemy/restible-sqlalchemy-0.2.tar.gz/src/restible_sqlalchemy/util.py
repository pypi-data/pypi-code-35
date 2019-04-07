# -*- coding: utf-8 -*-
""" Helpers for using SQLAlchemy with restible. """
from __future__ import absolute_import, unicode_literals

# stdlib imports
from typing import Any, Dict, Text

# local imports
from restible.util import QsFilter
from six import iteritems
from sqlalchemy.orm import Query


OP_MAP = {
    'eq': '__eq__',
    'ne': '__ne__',
    'lt': '__lt__',
    'gt': '__gt__',
    'le': '__le__',
    'ge': '__ge__',
    'in': 'in_',
}


def db_query_from_params(model_cls, params):
    # type: (Type, Dict[Text, Any]) -> Query
    """ Create SQLAlchemy query from a HTTP query params dict.

    This is a helper function to simplify the final resource actions
    implementations. Makes adding filtering to the query handlers dead simple.

    Args:
        model_cls (Type):
            The model class to query.
        params (dict[str, Any]):
            HTTP query string params as dictionary.

    Returns:
        Query:
            SQLAlchemy query corresponding to the given HTTP query params.

    Examples:

        >>> from restible_sqlalchemy.util import db_query_from_params
        >>> from flask_sqlalchemy import SQLAlchemy
        >>>
        >>> db = SQLAlchemy()
        >>>
        >>> class Person(db.Model):
        ...     name = db.Column(db.String(100))
        ...     age = db.Column(db.Integer)
        >>>
        >>> filters = {
        ...     'name': 'John',
        ...     'age': 32
        ... }
        >>> person = db_query_from_params(Person, filters).get()

    """
    filters = [QsFilter.build(OP_MAP, k, v) for k, v in iteritems(params)]
    db_filters = [flt(model_cls) for flt in filters]

    return model_cls.query.filter(*db_filters)


# Used only in type hint comments
del Any, Dict, Text, Query
