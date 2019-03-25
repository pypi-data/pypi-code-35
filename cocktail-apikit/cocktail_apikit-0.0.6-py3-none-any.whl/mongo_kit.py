"""
Common mongo db client toolkit used by api project
"""
import uuid
from datetime import datetime, timezone
from math import ceil
from typing import Any, Union, List, Dict
from urllib.parse import urlencode
from uuid import UUID

import pymongo
from bottle import BaseRequest
from bson import binary
from marshmallow import Schema
from pymongo import MongoClient, ReturnDocument
from pymongo.cursor import Cursor
from pymongo.errors import BulkWriteError, DuplicateKeyError
from pymongo.results import UpdateResult

from cocktail_apikit import MONGO_ID_FIELD_NAME
from .bottle_kit import ValidationError
from .constants import (
    SORT_KEY, PAGE_KEY, LIMIT_KEY, REQUEST_DESC_SORT_MARK,
    RECORD_ACTIVE_FLAG_FIELD, REQUEST_LOOKUP_MARK, MONGO_LOOKUPS_MAPPINGS
)

from .settings_kit import DefaultSettings


def _uuid_string_to_mongo_uuid(uuid_string):
    """
    Convert the UUID field value to be compatible with mongo
    """
    if isinstance(uuid_string, str):
        return binary.UUIDLegacy(UUID(uuid_string))
    if isinstance(uuid_string, UUID):
        return binary.UUIDLegacy(uuid_string)
    else:
        raise ValidationError('value "{}" should be a str or UUID type'.format(uuid_string))


def get_default_settings():
    from .settings_kit import DefaultSettings
    return DefaultSettings


class MongoQuery(object):
    """
    Class to represent to mongo query collections, which including:
        1. conditions: dict (used for query)
        2. projections: dict (used for project field)
        3. skip: int (used for slice)
        4. limit: int (used for slice)
        5. page: int (will be used by pagination)
        6. sort: list
        6. base_query_string: str (used by pagination)
    """

    def __init__(self,
                 conditions: dict = None,
                 projections: dict = None,
                 skip: int = 0,
                 limit: int = None,
                 page: int = 1,
                 sort: list = None,
                 base_query_string: str = ''):
        self.conditions = conditions or {}
        self.projections = projections or {}
        self.skip = skip
        self.limit = limit
        self.page = page
        self.sort = sort or []
        self.base_query_string = base_query_string

    def __setitem__(self, key, value):
        """
        Extra attribute will insert into conditions attribute  
        """
        self.conditions[key] = value

    def to_dict(self):
        self.conditions.update({
            'skip': self.skip,
            'limit': self.limit,
            'page': self.page,
            'sort': self.sort

        })
        return self.conditions


class BottleMongoQueryBuilder(object):
    """
    Builder to build a MongoQuery from bottle framework's request object
    """

    def __init__(self, request: BaseRequest = None, schema: Schema = None):
        self._bottle_params = request.params
        self.schema = schema
        self.conditions = {}
        self.sort = self._build_mongo_sort(
            self._bottle_params.getlist(SORT_KEY))
        self.page = self._get_page(self._bottle_params.pop(PAGE_KEY, 1))

        self.limit = self._get_limit(self._bottle_params.pop(LIMIT_KEY, DefaultSettings.API_DEFAULT_LIMIT))
        self.skip = (self.page - 1) * self.limit
        self._bottle_params.pop(SORT_KEY, None)
        self.builder_filter()
        self.validate_filter_and_sort()
        query_dict = request.query
        query_dict.pop(PAGE_KEY, None)
        self.base_query_string = '{}?{}'.format(
            request.fullpath, urlencode(query_dict))

    @staticmethod
    def _get_page(page):
        """
        fetch the page parameter from request query
        """
        try:
            page = int(page)
            return page if page > 0 else -page
        except ValueError:
            return 1

    @staticmethod
    def _get_limit(limit):
        """
        fetch the limit parameter from request query
        """
        try:
            limit = int(limit)
            return limit
        except:
            return DefaultSettings.API_DEFAULT_LIMIT

    @staticmethod
    def _build_mongo_sort(sort_fields: List[str] = None):
        """
        convert request sort field condition to mongo sort form
        """

        return [
            (field[1:], pymongo.DESCENDING) if field.startswith(
                REQUEST_DESC_SORT_MARK) else (field, pymongo.ASCENDING)
            for field in sort_fields
        ]

    def builder_filter(self):
        for raw_key, value in self._bottle_params.items():

            # make id value be compatible with mongo
            if raw_key.startswith('id'):
                raw_key = '_{}'.format(raw_key)
                value = _uuid_string_to_mongo_uuid(value)

            # simple field request without any extra operation
            if REQUEST_LOOKUP_MARK not in raw_key:
                self.conditions[raw_key] = value
                continue

            key, _, operator = raw_key.rpartition(REQUEST_LOOKUP_MARK)
            if operator not in MONGO_LOOKUPS_MAPPINGS:
                raise ValidationError(
                    "Query operator: '{}' does not exists!".format(operator))

            # Query by range, the list value is separated by ','
            if operator == 'in' and isinstance(value, str):
                value = value.split(',')

            self.conditions[key] = {
                MONGO_LOOKUPS_MAPPINGS.get(operator): value
            }

    def validate_filter_and_sort(self):
        """
        Validate if the client's request's query and sort fields are all valid
        """

        if not self.schema:
            return True

        valid_query_fields = self.schema.valid_mongo_query_fields()
        print(valid_query_fields)

        for field in self.conditions:
            if field not in valid_query_fields:
                raise ValidationError(
                    "Query field: '{}' is not a valid query field!".format(field))

        for field in self.sort:
            if field[0] not in valid_query_fields:
                raise ValidationError(
                    "Sort field: '{}' is not a valid sort field!".format(field[0]))

    def to_mongo_query(self) -> MongoQuery:
        return MongoQuery(
            conditions=self.conditions,
            projections=None,
            skip=self.skip,
            page=self.page,
            limit=self.limit,
            sort=self.sort,
            base_query_string=self.base_query_string
        )


class MongoDBManager(object):
    """
    Base Mongo manager to manage all communication with MongoDB
    """
    DB_CONFIG = None

    def __init__(self, config: dict = None):
        self.config = config or self.DB_CONFIG
        assert self.config, 'Mongo DB configuration object is required!'
        self.client = MongoClient(self.config['MONGODB_URI'])
        self._check_duplicate_db_name(self.config['DB_NAME'])
        self.db = self.client.get_database(self.config['DB_NAME'])
        self.collection = self.db.get_collection(self.config['COLLECTION_NAME'])

    def _check_duplicate_db_name(self, config_db_name):
        """
        validation the configuration DB_NAME key, to avoid the mongo case-insensitive database name error
        """
        db_names = {name.lower(): name for name in self.client.list_database_names()}
        if config_db_name.lower() in db_names and config_db_name != db_names[config_db_name.lower()]:
            raise Exception((
                'Configured DB_NAME: "{0}" duplicated with already existed DB_NAME: "{1}"'
                '.(Please change DB_NAME to another name or use the exist DB_NAME: "{1}")'.format(
                    config_db_name,
                    db_names[config_db_name.lower()]
                ))
            )

    def _convert_uuid_condition_value(self, condition):
        """
        Check if condition contains _id then convert it to mongo compatible UUIDLegacy
        """
        if condition.get(MONGO_ID_FIELD_NAME, None):
            condition[MONGO_ID_FIELD_NAME] = _uuid_string_to_mongo_uuid(condition.get(MONGO_ID_FIELD_NAME))
        return condition

    def update(self, condition: dict = None, changed_value: dict = None) -> (UpdateResult, dict):
        """
        Update the changed value and also update the updated_at field with default current time
        """
        condition = self._convert_uuid_condition_value(condition)

        changed_value.update(
            {'updated_at': datetime.now().astimezone(timezone.utc)})
        changed_value = {'$set': changed_value}
        try:
            return self.collection.update_many(condition, changed_value), {}
        except Exception as e:
            return None, {'msg': str(e)}

    def find_one_and_update(self, condition: dict = None, changed_value: dict = None, projection: dict = None,
                            sort: list = None, return_document: bool = ReturnDocument.AFTER):
        """
        Update one record which selected by conditions with the changed_value data 
        """
        condition = self._convert_uuid_condition_value(condition)
        changed_value.update(
            {'$set': {'updated_at': datetime.now().astimezone(timezone.utc)}})
        return self.collection.find_one_and_update(filter=condition, update=changed_value, projection=projection,
                                                   sort=sort, return_document=return_document)

    def filter(self, query: Union[MongoQuery, Dict] = None, soft_delete: bool = True) -> (Cursor, int):
        """
        Do mongo query search with given query object, 
        : param query: can be a MongoQuery object or dict object
        : param soft_delete: indicate if current delete strategy is soft delete or not to add an extra condition 
        """
        query = query.to_dict() if isinstance(query, MongoQuery) else query
        # print('query summary:', query)

        sort_fields = query.pop('sort', [])
        skip = query.pop('skip', 0)
        limit = query.pop('limit', DefaultSettings.API_DEFAULT_LIMIT)
        query.pop('page', 1)

        if soft_delete:
            query[RECORD_ACTIVE_FLAG_FIELD] = True

        count = self.collection.count_documents(query)
        results = self.collection.find(query)
        results = self.sort(results, sort_fields)
        results = self.slice(results, skip, limit)
        return results, count

    def sort(self, results: Cursor, sort_fields: Any) -> Cursor:
        """
        Sort the result by the given sort fields list 
        """
        if not sort_fields:
            return results
        results.sort(sort_fields)
        return results

    def slice(self, results: Cursor, skip: int = None, limit: int = None) -> Cursor:
        """
        Extract a slice from the queried results 
        """
        return results.skip(skip).limit(limit)

    def delete(self, condition: dict = None, soft_delete: bool = True) -> (UpdateResult, dict):
        """
        Delete record from mongodb by given delete condition

        :param soft_delete: Flag to indicate if delete action is hard deleted or not. If
                             soft_delete is true, then delete action is just set a flag, 
                             not delete forever

        """
        condition = self._convert_uuid_condition_value(condition)
        if not soft_delete:
            return self.collection.delete_many(condition)

        condition[RECORD_ACTIVE_FLAG_FIELD] = True
        soft_delete_mark = {'$set':
            {
                RECORD_ACTIVE_FLAG_FIELD: False,
                'deleted_at': datetime.now().astimezone(timezone.utc)
            }
        }
        try:
            return self.collection.update_many(condition, soft_delete_mark), {}

        except Exception as e:
            return None, {'errors': str(e)}

    def create(self, data: Union[List[Dict], Dict] = None, soft_delete: bool = True) -> (list, dict):
        """ Insert one or many record into MongoDB

        :param soft_delete: If set to True, then added an extra indicator field to database 
        """
        if not data or (isinstance(data, list) and not data[0]):
            return [], {'errors': 'Empty data'}

        if not isinstance(data, list):
            data = [data]

        for obj in data:

            if soft_delete and RECORD_ACTIVE_FLAG_FIELD not in obj:
                obj[RECORD_ACTIVE_FLAG_FIELD] = True

        try:
            return [id for id in self.collection.insert_many(data).inserted_ids], {}

        except (BulkWriteError, DuplicateKeyError) as e:
            return [], {'errors': str(e)}


class Pagination:
    """
    Used to render a list of object with pagination metadata included
    """

    def __init__(self, query: MongoQuery, objects: Cursor, count: int):
        self.query = query
        self.objects = list(objects)
        self.count = count
        self.pages = ceil(self.count / self.query.limit)

    def serialize(self, schema: Schema = None):
        """
        Create the final serialized result data
        """
        return {
            'pagination': {
                'limit': self.query.limit,
                'page': self.query.page,
                'total_pages': ceil(self.count / self.query.limit),
                'total_count': self.count,
                'next_url': self.next_page_url,
                'previous_url': self.previous_page_url,
            },
            'objects': self._dump_object_by_schema(self.objects, schema)
        }

    @staticmethod
    def _dump_object_by_schema(objects: list = None, schema: Schema = None):
        if not schema:
            return objects

        serialized_data, errors = schema.dump(objects, many=True)
        if errors:
            raise ValidationError(str(errors))
        return serialized_data

    def has_next_page(self):
        return self.query.page < self.pages

    def has_previous_page(self):
        return self.query.page > 1

    @property
    def next_page_url(self):
        if not self.has_next_page():
            return None
        return self.query.base_query_string + '&page={}'.format(self.query.page + 1)

    @property
    def previous_page_url(self):
        if not self.has_previous_page():
            return None
        return self.query.base_query_string + '&page={}'.format(self.query.page - 1)


if __name__ == '__main__':
    pass
    # config = DefaultSettings.mongo_config_for_collection()
    # print(config)
    # db = MongoDBManager(DefaultSettings.mongo_db_config())
    # db = DefaultMongoDBManager()
