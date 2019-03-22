# -*- coding: utf-8 -*-

import peewee
from peewee_async import Manager

from facture.exceptions import FactureException
from .base import BaseService


class DatabaseService(BaseService):
    """Service class providing an interface with common database operations

    :ivar __model__: Peewee.Model
    :ivar db_manager: Facture database manager (peewee-async)
    """

    __model__: peewee.Model
    db_manager: Manager

    @classmethod
    def register(cls, pkg, mgr):
        super(DatabaseService, cls).register(pkg, mgr)
        cls.db_manager = mgr.db.manager

    @property
    def model(self):
        """Return service model or raise an exception

        :return: peewee.Model
        """

        if not self.__model__:
            raise Exception(f'{self.__class__.__name__}.__model__ not set, unable to perform database operation')

        return self.__model__

    def _select(self, *fields):
        """Creates a new select query

        :param fields: fields tuple
        :return: peewee.ModelSelect
        """

        return self.model.extended(*fields) if hasattr(self.model, 'extended') else self.model.select(*fields)

    def _model_has_attrs(self, *attrs):
        """Ensure model has field(s)

        :param attrs: fields tuple
        :return: True or Exception
        """

        for attr in attrs:
            if not hasattr(self.model, attr):
                raise Exception(f'Unknown field {attr}', 400)

        return True

    def _parse_sortstr(self, value: str):
        """Takes a comma-separated string of fields to sort in asc or desc order

        example: "-field1,field2" to order by field1 desc, field2 asc

        :param value: sortstr
        :return: list of sort-objects
        """

        if not value:
            return []

        model = self.model

        for col_name in value.split(','):
            sort_asc = True
            if col_name.startswith('-'):
                col_name = col_name[1:]
                sort_asc = False

            if self._model_has_attrs(col_name):
                sort_obj = getattr(model, col_name)
                yield sort_obj.asc() if sort_asc else sort_obj.desc()

    def _get_query_filtered(self, expression: peewee.Expression = None, select: peewee.ModelSelect = None, **params):
        """Constructs a query using an Expression and/or parameters.

        :param expression: peewee.Expression
        :param select: peewee.ModelSelect
        :param params: Dictionary for controlling pagination and sorting
        :return: Peewee query
        """

        query_base = select or self._select()

        sort = params.pop('_sort', None)
        limit = params.pop('_limit', 0)
        offset = params.pop('_offset', 0)

        query = query_base.limit(limit).offset(offset)

        if isinstance(expression, peewee.Expression):
            query = query.where(expression)
        elif params:
            query = query.filter(**params)

        if sort:
            order = self._parse_sortstr(params['sort'])
            return query.order_by(*order)

        return query

    async def get_many(self, expression=None, **kwargs):
        """Returns a list of zero or more records

        :param expression: peewee.Expression (optional)
        :param kwargs: kwargs to pass along to `_get_query_filtered`
        :return: [peewee.Model]
        """

        query = self._get_query_filtered(expression, **kwargs)
        return [o for o in await self.db_manager.execute(query)]

    async def get_by_pk(self, record_id: int):
        """Returns the matching record or raises an exception

        :param record_id: the record to query for
        :return: peewee.Model
        """

        return await self.get_one(self.__model__.id == record_id)

    async def create(self, item: dict):
        """Creates new record, returning the record upon success

        :param item: item to be inserted
        :return: peewee.Model
        """

        return await self.db_manager.create(self.model, **item)

    async def get_or_create(self, item: dict):
        """Get an object or create it with the provided defaults

        :param item: item to be fetched or inserted
        :return: peewee.Model
        """

        return await self.db_manager.get_or_create(self.model, **item)

    async def count(self, expression=None, **kwargs):
        """Return the number of records the given query would yield

        :param expression: peewee.Expression (optional)
        :param kwargs: kwargs to pass along to `_get_query_filtered`
        :return: count (int)
        """

        query = self._get_query_filtered(expression, **kwargs)
        return await self.db_manager.count(query)

    async def get_one(self, *args, **kwargs):
        """Get exactly one record or raise an exception

        :param args: peewee.Expression (optional)
        :param kwargs: kwargs to pass along to `_get_query_filtered`
        :return: peewee.Model
        """

        query = self._get_query_filtered(*args, **kwargs)

        try:
            return await self.db_manager.get(query)
        except peewee.DoesNotExist:
            raise FactureException('No such record', 404)

    async def update(self, record, payload):
        """Updates a record in the database

        :param record: peewee.Model or PK
        :param payload: update payload
        :return: updated record
        """

        if not isinstance(record, peewee.Model):
            record = await self.get_by_pk(record)

        for k, v in payload.items():
            setattr(record, k, v)

        await self.db_manager.update(record)
        return record

    async def delete(self, record_id: int):
        """Deletes a record by id

        :param record_id: record id
        :return: {'deleted': True|False}
        """

        record = await self.get_by_pk(record_id)
        deleted = await self.db_manager.delete(record)
        return {'deleted': deleted}
