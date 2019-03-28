#!-*- coding:utf-8 -*-

from bson import ObjectId
from kmux_mongo.kmux_mongo import KmuxMongo


class KmuxModel(object):
    def __init__(self, mongo_client, collection_name, pk_name='_id', ex_field_names=None, **kw):
        assert isinstance(mongo_client, KmuxMongo)
        assert isinstance(collection_name, str)
        self._mongo_client = mongo_client
        self._collection_name = collection_name
        self._pk_name = pk_name
        self._ex_field_names = KmuxModel._process_ex_field_names(ex_field_names)

    @staticmethod
    def _process_ex_field_names(d):
        ret = d if isinstance(d, dict) else dict()
        ret.setdefault('created_time', 'created_time')
        ret.setdefault('updated_time', 'updated_time')
        ret.setdefault('is_deleted', '__is_deleted__')
        return ret

    @property
    def mongo_client(self):
        return self._mongo_client

    @property
    def collection_name(self):
        return self._collection_name  # type: str

    @property
    def ex_field_created_time(self):
        return self._ex_field_names.get('created_time', 'created_time')

    @property
    def ex_field_updated_time(self):
        return self._ex_field_names.get('updated_time', 'updated_time')

    @property
    def ex_field_is_deleted(self):
        return self._ex_field_names.get('is_deleted', '__is_deleted__')

    @property
    def pk_name(self):
        return self._pk_name  # type: str

    @staticmethod
    def delete_dict_k_safe(d, k):
        v = None
        if k in d:
            v = d[k]
            del d[k]
        return v

    def process_filter_for_not_deleted(self, filter):
        assert isinstance(filter, dict)
        new_filter = {
            '$and': [
                {
                    self.ex_field_is_deleted: {'$ne': True},
                },
                filter,
            ]
        }
        return new_filter

    def insert_item(self, item):
        assert isinstance(item, dict)
        self.delete_dict_k_safe(item, self.ex_field_is_deleted)

        item['_id'] = item.get('_id', ObjectId())
        item[self.ex_field_created_time] = self.mongo_client.current_time
        item[self.ex_field_updated_time] = self.mongo_client.current_time

        self.mongo_client.insert_one(self.collection_name, item)

        return item

    def delete_item(self, filter):
        filter = self.process_filter_for_not_deleted(filter)
        self.mongo_client.update_one(self.collection_name, filter, {
            '$set': {self.ex_field_is_deleted, True}
        })

    def delete_item_by_property(self, property_name, property_value):
        self.delete_item({
            property_name: property_value,
        })

    def delete_item_by_pk(self, pk_value):
        self.delete_item_by_property(property_name=self.pk_name, property_value=pk_value)

    def update_item(self, filter, update, upsert=False):
        filter = self.process_filter_for_not_deleted(filter)

        assert isinstance(update, dict)
        set_table = update.get('$set', {})
        set_table[self.ex_field_updated_time] = self.mongo_client.current_time
        update['$set'] = set_table

        self.mongo_client.update_one(self.collection_name, filter, update, upsert)

    def update_items(self, filter, update, upsert=False):
        filter = self.process_filter_for_not_deleted(filter)

        assert isinstance(update, dict)
        set_table = update.get('$set', {})
        set_table[self.ex_field_updated_time] = self.mongo_client.current_time
        update['$set'] = set_table

        self.mongo_client.update_many(self.collection_name, filter, update, upsert)

    def update_item_by_property(self, property_name, property_value, update):
        self.update_item({
            property_name: property_value,
        }, update)

    def update_item_by_pk(self, pk_value, update):
        self.update_item_by_property(self.pk_name, pk_value, update)

    def set_item_property(self, pk_value, property_name, property_value):
        self.update_item_by_pk(pk_value, {
            '$set': {
                property_name: property_value,
            },
        })

    def inc_item_property(self, pk_value, property_name, property_value):
        self.update_item_by_pk(pk_value, {
            '$inc': {
                property_name: property_value,
            },
        })

    def push_item_property(self, pk_value, property_name, property_value):
        self.update_item_by_pk(pk_value, {
            '$push': {
                property_name: property_value,
            },
        })

    def pull_item_property(self, pk_value, property_name, property_value):
        self.update_item_by_pk(pk_value, {
            '$pull': {
                property_name: property_value,
            },
        })

    def update_item_properties(self, pk_value, set_properties=None, inc_properties=None, push_properties=None, pull_properties=None):
        update = dict()
        if isinstance(set_properties, dict) and len(set_properties):
            update['$set'] = set_properties
        if isinstance(inc_properties, dict) and len(inc_properties):
            update['$inc'] = inc_properties
        if isinstance(push_properties, dict) and len(push_properties):
            update['$push'] = push_properties
        if isinstance(pull_properties, dict) and len(pull_properties):
            update['$pull'] = pull_properties
        if len(update):
            self.update_item_by_pk(pk_value, update)

    def set_item_properties(self, pk_value, **kw):
        self.update_item_properties(pk_value, set_properties=kw)

    def inc_item_properties(self, pk_value, **kw):
        self.update_item_properties(pk_value, inc_properties=kw)

    def push_item_properties(self, pk_value, **kw):
        self.update_item_properties(pk_value, push_properties=kw)

    def pull_item_properties(self, pk_value, **kw):
        self.update_item_properties(pk_value, pull_properties=kw)

    def find_item(self, filter, default=None):
        filter = self.process_filter_for_not_deleted(filter)
        item = self.mongo_client.find_one(self.collection_name, filter)
        item = default if item is None else item
        return item

    def find_item_random(self, filter, default=None):
        filter = self.process_filter_for_not_deleted(filter)
        item = self.mongo_client.find_one_random(self.collection_name, filter)
        item = default if item is None else item
        return item

    def find_item_by_property(self, property_name, property_value):
        return self.find_item({
            property_name: property_value,
        })

    def find_item_by_pk(self, pk_value):
        return self.find_item_by_property(self.pk_name, pk_value)

    def find_items_with_page_info(self, filter, sort=None, limit=None, page_info=None):
        filter = self.process_filter_for_not_deleted(filter)
        items, page_info = self.mongo_client.find_many_with_page_info(
            self.collection_name,
            filter=filter,
            sort=sort,
            limit=limit,
            page_info=page_info,
        )
        return items, page_info

    def find_items(self, filter, sort=None):
        items, page_info = self.find_items_with_page_info(filter, sort)
        return items

    def find_items_by_pk_as_table(self, pk_values, pk_name=None):
        assert isinstance(pk_values, (set, list, tuple))
        pk_name = self.pk_name if pk_name is None else pk_name
        items = self.find_items({
            pk_name: {'$in': list(pk_values)},
        })
        table = dict()
        for item in items:
            if pk_name in item:
                table[item[pk_name]] = item
        return table

    def find_items_by_pk_as_order(self, pk_values, pk_name=None):
        table = self.find_items_by_pk_as_table(pk_values=pk_values, pk_name=pk_name)
        items = [table[x] for x in pk_values if x in table]
        return items

    def is_exists(self, filter):
        return bool(self.find_item(filter))

    def is_exists_by_propery(self, property_name, property_value):
        return bool(self.find_item_by_property(property_name, property_value))

    def is_exists_by_pk(self, pk_value):
        return bool(self.find_item_by_pk(pk_value))
