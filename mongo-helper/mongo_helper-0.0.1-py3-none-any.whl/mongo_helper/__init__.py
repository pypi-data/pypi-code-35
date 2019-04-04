import settings_helper as sh
import dt_helper as dh
from collections import OrderedDict
from contextlib import suppress
from pymongo import MongoClient
from bson.objectid import ObjectId


get_setting = sh.settings_getter(__name__)
mongo_url = get_setting('mongo_url')


def get_date_query(date_string, fmt='%Y-%m-%d', timezone="America/Chicago",
                   timestamp_field='_id'):
    """Return a dict representing a query for matching date in a timezone

    - fmt: format the date_string is in
    - timezone: timezone to use for determining start of day
    - timestamp_field: name of timestamp field to query on
    """
    dt = dh.date_start_utc(date_string, fmt, timezone)
    query = {timestamp_field: {}}
    start = dt
    end = dt + dh.timedelta(days=1)
    if timestamp_field == '_id':
        start = ObjectId.from_datetime(start)
        end = ObjectId.from_datetime(end)
    query[timestamp_field]['$gte'] = start
    query[timestamp_field]['$lt'] = end
    return query


def get_days_ago_query(days_ago=0, until_days_ago=0, timezone="America/Chicago",
                       timestamp_field='_id'):
    """Return a dict representing a query for matching day(s) in a timezone

    - timestamp_field: name of timestamp field to query on
    """
    assert days_ago >= until_days_ago
    if days_ago > 0:
        assert days_ago != until_days_ago
    query = {timestamp_field: {}}
    start = dh.days_ago(days_ago, timezone=timezone)
    end = dh.days_ago(until_days_ago, timezone=timezone)
    if timestamp_field == '_id':
        start = ObjectId.from_datetime(start)
        end = ObjectId.from_datetime(end)
    query[timestamp_field]['$gte'] = start
    if days_ago > 0:
        query[timestamp_field]['$lt'] = end
    return query


def get_hours_ago_query(hours_ago=1, until_hours_ago=0, timestamp_field='_id'):
    """Return a dict representing a query for matching hour(s)

    - timestamp_field: name of timestamp field to query on
    """
    assert hours_ago > until_hours_ago
    now = dh.utc_now_localized()
    query = {timestamp_field: {}}
    start = now - dh.timedelta(hours=hours_ago)
    end = now - dh.timedelta(hours=until_hours_ago)
    if timestamp_field == '_id':
        start = ObjectId.from_datetime(start)
        end = ObjectId.from_datetime(end)
    query[timestamp_field]['$gte'] = start
    query[timestamp_field]['$lt'] = end
    return query


def get_minutes_ago_query(minutes_ago=1, until_minutes_ago=0, timestamp_field='_id'):
    """Return a dict representing a query for matching minute(s)

    - timestamp_field: name of timestamp field to query on
    """
    assert minutes_ago > until_minutes_ago
    now = dh.utc_now_localized()
    query = {timestamp_field: {}}
    start = now - dh.timedelta(minutes=minutes_ago)
    end = now - dh.timedelta(minutes=until_minutes_ago)
    if timestamp_field == '_id':
        start = ObjectId.from_datetime(start)
        end = ObjectId.from_datetime(end)
    query[timestamp_field]['$gte'] = start
    query[timestamp_field]['$lt'] = end
    return query


class Mongo(object):
    def __init__(self, url=None):
        """An instance that can execute MongoDB statements

        - url: connection url to a MongoDB
        """
        self._client = MongoClient(url)

    def get_collections(self):
        """Return a list of collection names"""
        return self._client.db.list_collection_names()

    def _find(self, collection, *args, **kwargs):
        """Return a cursor"""
        return self._client.db[collection].find(*args, **kwargs)

    def _find_one(self, collection, *args, **kwargs):
        """Return an object"""
        return self._client.db[collection].find_one(*args, **kwargs)

    def _count(self, collection, *args, **kwargs):
        """Return an int"""
        return self._client.db[collection].count(*args, **kwargs)

    def _aggregate(self, collection, *args, **kwargs):
        """Return a cursor"""
        return self._client.db[collection].aggregate(*args, **kwargs)

    def _index_information(self, collection):
        """Return a dict of info about indexes on collection"""
        try:
            index_info = self._client.db[collection].index_information()
        except:
            index_info = {}
        return index_info

    def last_obj(self, collection, timestamp_field='_id', **kwargs):
        """Return last object inserted to collection

        - timestamp_field: name of timestamp field to sort on
        - kwargs: passed to `self._find_one`
        """
        if 'sort' not in kwargs:
            kwargs['sort'] = [(timestamp_field, -1)]

        return self._find_one(collection, **kwargs)

    def first_obj(self, collection, timestamp_field='_id', **kwargs):
        """Return first object inserted to collection

        - timestamp_field: name of timestamp field to sort on
        - kwargs: passed to `self._find_one`
        """
        if 'sort' not in kwargs:
            kwargs['sort'] = [(timestamp_field, 1)]

        return self._find_one(collection, **kwargs)

    def obj_id_set(self, collection, match):
        """Return set of ObjectIds for match

        - match: dictionary representing the documents to match
        """
        return set([
            x['_id']
            for x in self._find(collection, match, projection=['_id'])
        ])

    def ez_pipeline(self, collection, match, group_by, timestamp_field='_id',
                    projection=None, limit=None, to_set=None, to_list=None,
                    to_sum=None, group_action=None, include_condition=None,
                    verbose=False):
        """Build/run an aggregation pipeline to group and count data

        - collection: name of collection
        - match: dictionary representing the "match stage"
        - group_by: list of keys to group by
        - timestamp_field: name of timestamp field to sort on (if 'limit' != None)
        - projection: list of keys to project
        - limit: max number of items
        - to_set: list of keys, where each key will have its values added to a
          set for each unique group
        - to_list: list of keys, where each key will have its values added to a
          list for each unique group
        - to_sum: list of keys, where each key will have its values summed
          for each unique group

        (After aggregation)
        - group_action: callable that will be mapped over each grouped item
        - include_condition: callable returning a bool to determine if a grouped
          item will be included in returned data
        - verbose: if True, print the generated pipeline command

        Return a dictionary with keys 'counts', 'data', 'total', 'group_by',
        'duration', 'pipeline', and 'total_percent'.
        """
        _start = dh.utc_now_localized()
        pipeline = [{'$match': match}]

        if limit:
            pipeline.append({'$sort': {timestamp_field: -1}})
            pipeline.append({'$limit': limit})

        if projection:
            pipeline.append({'$project': {k: '${}'.format(k) for k in projection}})

        group = {
            '$group': {
                '_id': {k: '${}'.format(k) for k in group_by},
                'count': {'$sum': 1},
            }
        }
        if to_set:
            group['$group'].update({
                k: {'$addToSet': '${}'.format(k)} for k in to_set
            })
        if to_list:
            group['$group'].update({
                k: {'$push': '${}'.format(k)} for k in to_list
            })
        if to_sum:
            group['$group'].update({
                k: {'$sum': '${}'.format(k)} for k in to_sum
            })
        pipeline.append(group)
        pipeline.append({'$sort': {'count': -1}})

        if verbose:
            from pprint import pprint
            pprint(pipeline)

        cursor = self._aggregate(collection, pipeline)
        counts = []
        data = {}
        total = 0

        if include_condition is None:
            include_condition = lambda x: True
        elif not callable(include_condition):
            include_condition = lambda x: True

        for item in cursor:
            count = item.pop('count')
            total += count

            if include_condition(item):
                the_group = tuple([item['_id'].get(k, '') for k in group_by])
                with suppress(TypeError):
                    item = group_action(item)
                counts.append((the_group, count))
                data[the_group] = item

        final_counts = {'data': []}
        for name, count in counts:
            final_counts['data'].append((name, count, count/total))

        final_data = OrderedDict()
        for x in final_counts['data']:
            key = x[0]
            final_data[key] = data[key]

        total_percent = sum([x[-1] for x in final_counts['data']])

        _end = dh.utc_now_localized()

        results = {
            'counts': final_counts,
            'data': final_data,
            'total': total,
            'total_percent': total_percent,
            'group_by': tuple(group_by),
            'duration': (_end - _start).total_seconds(),
            'pipeline': pipeline,
        }
        return results
