# -*- coding:utf-8 -*-

import random
import pymongo
from bson import ObjectId
from datetime import datetime
from collections import OrderedDict


class KmuxMongo(object):
    def __init__(self, host='localhost', port=27017, username=None, password=None, database='admin', current_time=None):
        if isinstance(host, str):
            if '://' in host:
                py_mongo_client = KmuxMongo.create_py_mongo_client_from_url(host)
            else:
                py_mongo_client = KmuxMongo.create_py_mongo_client(host, port, username, password)
        else:
            assert isinstance(host, pymongo.MongoClient)
            py_mongo_client = host
        self._mongo_db = py_mongo_client.get_database(database)
        self._current_time = None

        self.current_time = current_time

    @staticmethod
    def create_py_mongo_client(host='localhsot', port=27017, username=None, password=None):
        py_mongo_client = pymongo.MongoClient(
            host=host,
            port=port,
            username=username,
            password=password,
        )
        return py_mongo_client

    @staticmethod
    def create_py_mongo_client_from_url(url='mongodb://localhost:27017/admin'):
        py_mongo_client = pymongo.MongoClient(url)
        return py_mongo_client

    @property
    def db(self):
        return self._mongo_db  # type: pymongo.database

    @property
    def mongo_db(self):
        return self._mongo_db

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, v):
        self._current_time = v if isinstance(v, datetime) else datetime.now()

    @staticmethod
    def _preprocess_sort(sort):
        items = []
        if isinstance(sort, (tuple, list)):
            if len(sort) == 2 and isinstance(sort[0], str) and sort[1] in [1, -1]:
                items = [tuple(sort)]
            else:
                for item in sort:
                    if isinstance(item, (tuple, list)) and len(item) == 2 and isinstance(item[0], str) and item[1] in [1, -1]:
                        items.append(tuple(item))
        elif isinstance(sort, OrderedDict):
            for (k, v) in sort.iteritems():
                if isinstance(k, str) and v in [1, -1]:
                    items.append((k, v))

        items = items if len(items) else None
        return items

    def aggregate(self, collection_name, pipeline):
        items = []
        cursor = self.db.get_collection(collection_name).aggregate(pipeline)
        for item in cursor:
            items.append(item)
        return items  # type: list[dict]

    def aggregate_one(self, collection_name, pipeline):
        cursor = self.db.get_collection(collection_name).aggregate(pipeline)
        for item in cursor:
            return item
        return None  # type: dict | None

    def count(self, collection_name, filter=None):
        count = self.db.get_collection(collection_name).count(filter)
        return count  # type: int

    def exists(self, collection_name, filter=None):
        item = self.db.get_collection(collection_name).find_one(filter)
        is_exists = item is not None
        return is_exists  # type: bool

    def find_one(self, collection_name, filter=None, sort=None, projection=None, fn_process_item=None):
        sort = self._preprocess_sort(sort)

        item = self.db.get_collection(collection_name).find_one(filter, sort=sort, projection=projection)
        if callable(fn_process_item) and item:
            item = fn_process_item(item)

        return item  # type: dict

    def find_many(self, collection_name, filter=None, sort=None, skip=None, limit=None, projection=None, fn_process_item=None):
        sort = self._preprocess_sort(sort)

        items = []
        if (isinstance(limit, int) and limit > 0) or limit is None:
            kw = dict()
            if sort:
                kw['sort'] = sort
            if isinstance(skip, int):
                kw['skip'] = skip
            if isinstance(limit, int):
                kw['limit'] = limit
            if projection:
                kw['projection'] = projection
            cursor = self.db.get_collection(collection_name).find(filter, **kw)
            if callable(fn_process_item):
                items = [fn_process_item(item) for item in cursor]
            else:
                items = [item for item in cursor]

        return items  # type: list[dict]

    def find_one_random(self, collection_name, filter=None, projection=None, fn_process_item=None):
        kw = dict()
        if projection:
            kw['projection'] = projection

        cursor = self.db.get_collection(collection_name).find(filter, **kw)
        item = None
        total = cursor.count()
        if total > 0:
            index = random.randint(0, max(total, 999999)) % total
            cursor.skip(index)
            item = cursor.next()

        if callable(fn_process_item) and item:
            item = fn_process_item(item)

        return item  # type: dict

    def insert_one(self, collection_name, document):
        assert isinstance(document, dict)
        result = self.db.get_collection(collection_name).insert_one(document)
        return result  # type: pymongo.results.InsertOneResult

    def insert_many(self, collection_name, documents):
        assert isinstance(documents, list)
        result = self.db.get_collection(collection_name).insert_many(documents)
        return result  # type: pymongo.results.InsertManyResult

    def delete_one(self, collection_name, filter):
        result = self.db.get_collection(collection_name).delete_one(filter)
        return result  # type: pymongo.results.DeleteOneResult

    def delete_many(self, collection_name, filter):
        result = self.db.get_collection(collection_name).delete_many(filter)
        return result  # type: pymongo.results.DeleteManyResult

    def update_one(self, collection_name, filter, update, upsert=False):
        result = self.db.get_collection(collection_name).update_one(filter, update, upsert)
        return result  # type: pymongo.results.UpdateOneResult

    def update_one_and_return_it(self, collection_name, filter, update, upsert=False):
        result = self.update_one(collection_name, filter, update, upsert)
        if upsert and result.upserted_id:
            return self.find_one(collection_name, {
                '_id': result.upserted_id
            })
        return self.find_one(collection_name, filter)  # type: dict | None

    def update_many(self, collection_name, filter, update, upsert=False):
        result = self.db.get_collection(collection_name).update_many(filter, update, upsert)
        return result  # type: pymongo.results.UpdateManyResult

    def find_one_and_delete(self, collection_name, filter, projection=None, sort=None, fn_process_item=None):
        sort = self._preprocess_sort(sort)

        item = self.db.get_collection(collection_name).find_one_and_delete(filter, projection, sort)
        if callable(fn_process_item) and item:
            item = fn_process_item(item)
        return item  # type: dict | None

    def find_one_and_replace(self, collection_name, filter, replacement, projection=None, sort=None, upsert=False, return_document=False, fn_process_item=None):
        sort = self._preprocess_sort(sort)

        item = self.db.get_collection(collection_name).find_one_and_replace(filter, replacement, projection, sort, upsert, return_document)
        if callable(fn_process_item) and item:
            item = fn_process_item(item)
        return item  # type: dict | None

    def find_one_and_update(self, collection_name, filter, update, projection=None, sort=None, upsert=False, return_document=False, fn_process_item=None):
        sort = self._preprocess_sort(sort)

        item = self.db.get_collection(collection_name).find_one_and_update(filter, update, projection, sort, upsert, return_document)
        if callable(fn_process_item) and item:
            item = fn_process_item(item)
        return item  # type: dict | None

    def find_many_with_page_info(self, collection_name, filter={}, sort=None, skip=None, limit=None, projection=None, page_info=None, fn_process_item=None, fn_process_sort=None):
        sort = self._preprocess_sort(sort)

        page_info = page_info if isinstance(page_info, dict) else dict()

        total = page_info.get('total', None)
        page_num = page_info.get('page_num', None)
        next_index = page_info.get('next_index', 0)
        cut_off_time = page_info.get('cut_off_time', self.current_time)

        filter = filter.copy()
        if '_id' in filter:
            filter['_id'] = {
                '$and': [
                    {'$lte': ObjectId.from_datetime(cut_off_time)},
                    filter['_id'],
                ]
            }
        else:
            filter['_id'] = {'$lte': ObjectId.from_datetime(cut_off_time)}

        if total is None:
            total = self.count(collection_name, filter=filter)

        if sort and callable(fn_process_sort):
            sort_t = fn_process_sort(sort)
        else:
            sort_t = sort

        if not isinstance(skip, int):
            skip = 0

        items = self.find_many(collection_name, filter=filter, sort=sort_t, skip=next_index + skip, limit=limit, projection=projection)

        page_num = 0 if page_num is None else page_num + 1
        from_index = next_index + skip
        next_index = next_index + skip + len(items)
        has_more = next_index < total

        page_info = dict(
            total=total,
            limit=limit,
            page_num=page_num,
            from_index=from_index,
            next_index=next_index,
            cut_off_time=cut_off_time,
            has_more=has_more,
        )

        if callable(fn_process_item) and items:
            for i in range(len(items)):
                items[i] = fn_process_item(items[i])

        return items, page_info  # type: list[dict], dict

    def collection_names(self, include_system_collections=True, session=None):
        return self.db.collection_names(include_system_collections, session)

    def create_collection(self, name, codec_options=None, read_preference=None, write_concern=None, read_concern=None, session=None, **kw):
        return self.db.create_collection(name, codec_options, read_preference, write_concern, read_concern, session, **kw)
