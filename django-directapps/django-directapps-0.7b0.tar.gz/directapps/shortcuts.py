#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from functools import reduce
from operator import or_ as OR

from django.db.models import Q
from django.shortcuts import _get_queryset


def smart_search(klass, fields, query):
    """
    Returns a filtered set of data.

    Parameter `klass` may be Model, Manager or QuerySet object. If there is no
    list of fields 'fields' or there is no search string 'query', then returns
    the data set as is.
    """
    queryset = _get_queryset(klass)

    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    if fields:
        lookups = [construct_search(str(f)) for f in fields]
        if query not in ('', None, False, True):
            for bit in query.split():
                queries = [Q(**{lookup: bit}) for lookup in lookups]
                queryset = queryset.filter(reduce(OR, queries))

    return queryset


def get_object_or_none(klass, *args, **kwargs):
    """
    Returns an object or None if the object does not exist. Always returns
    None if more than one object is found.

    Parameter `klass` may be Model, Manager or QuerySet object. All other
    parameters passed in are used for the query.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
    except queryset.model.MultipleObjectsReturned:
        return None
