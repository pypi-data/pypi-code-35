# -*- coding: utf-8 -*-
"""
Base class for resources using Google AppEngine ndb as storage.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from logging import getLogger

# 3rd party imports
from restible import util
from restible.model import ModelResource
from serafin import Fieldspec
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# local imports
from .util import db_query_from_params


L = getLogger(__name__)


class SqlAlchemyResource(ModelResource):
    """ Base class for ndb based resources.

    This provides a basic implementation that can be used out of the box. It
    provides no authentication/authorization.
    """
    name = None
    model = None
    spec = Fieldspec('*')
    schema = {}
    read_only = []
    _public_props = None
    _db_session = None

    @classmethod
    def init_session(cls, db_session):
        """ Initialize SQLAlchemy resources. """
        cls._db_session = db_session

    @property
    def db_session(self):
        """ Property returning the current SQLAlchemy session.

        Will try to get it from ``self.model.query.session`` as this is where
        flask has it.
        """
        if hasattr(self.model, 'query'):
            return self.model.query.session
        else:
            return self._db_session

    def create_item(self, request, params, payload):
        """ Create new model item. """
        del request, params     # Unused here

        try:
            item = self.model(**payload)

            self.db_session.add(item)
            self.db_session.commit()

            return item
        except IntegrityError:
            self.db_session.rollback()
            raise ModelResource.AlreadyExists()
        except SQLAlchemyError:
            self.db_session.rollback()
            raise

    def update_item(self, request, params, payload):
        del params      # Unused here

        item = self.item_for_request(request)
        if item is None:
            return None

        payload.pop('id', None)
        util.update_from_values(item, payload)

        try:
            self.db_session.commit()
        except SQLAlchemyError:
            self.db_session.rollback()
            raise

        return item

    def delete_item(self, request, params, payload):
        del params, payload     # Unused here

        item = self.item_for_request(request)
        if item:
            try:
                self.db_session.delete(item)
                self.db_session.commit()
            except SQLAlchemyError:
                self.db_session.rollback()
                raise

    def query_items(self, request, params, payload):
        """ Return a model query with the given filters.

        The query can be further customised like any ndb query.

        :return google.appengine.ext.ndb.Query:
            The query with the given filters already applied.
        """
        del request, payload     # Unused here
        return db_query_from_params(self.model, params).all()

    def get_item(self, request, params, payload):
        """ Get requested item. """
        del params, payload     # Unused here
        return self.item_for_request(request)

    def item_for_request(self, request):
        """ Get requested item. """
        pk = int(self.get_pk(request))
        return self.model.query.filter(self.model.id == pk).one_or_none()
