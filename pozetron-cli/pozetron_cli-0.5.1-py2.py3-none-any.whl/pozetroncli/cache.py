import json
import logging
import os.path as op
import shutil
from datetime import datetime
from calendar import timegm

from dictdiffer import diff, patch

from pozetroncli.conf import get_cache_filename, get_cache_tags_filename
from pozetroncli.utils import makedirs


logger = logging.getLogger('verbose')


class CacheError(Exception):
    pass


class CacheErrorBadRemoteData(Exception):
    pass


class CacheTagsStore(object):
    '''
    Class for storing most recent header cache tags coming from server
    '''

    def __init__(self):
        self._data = {
            'user_cache_tag': '',
            'global_cache_tag': ''
        }
        try:
            with open(get_cache_tags_filename()) as file:
                try:
                    # Note: we are updating self._data with file content rather than overriding it
                    # to ensure inner _data keys always exist
                    self._data.update(json.load(file))
                except ValueError:
                    pass
        except (IOError, OSError) as ex:
            if ex.args[0] != 2:  # FileNotFoundError
                raise
        self._modified = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def __setattr__(self, key, value):
        # Public attributes are stored in self._data, private ones are handled ordinarily
        if key.startswith('_'):
            self.__dict__[key] = value
        else:
            if key in self._data.keys():
                self._data[key] = value
                self._modified = True
            else:
                raise AttributeError('No attribute {0} found!'.format(key))

    def __getattr__(self, key):
        # Public attributes are looked up inside self._data, private ones are handled ordinarily
        if key.startswith('_'):
            return self.__dict__.get(key, None)
        if key in self._data.keys():
            return self._data[key]
        else:
            raise AttributeError('No attribute {0} found!'.format(key))

    def save(self, force=False):
        if self._modified or force:
            makedirs(op.dirname(get_cache_tags_filename()), exist_ok=True)
            tmp_filename = get_cache_tags_filename() + '.tmp'
            with open(tmp_filename, 'w') as file:
                json.dump(self._data, file)
            shutil.move(tmp_filename, get_cache_tags_filename())


class CacheStore(object):
    '''
    Class for managing local cache data
    '''

    def __init__(self):
        self._data = {
            'global': {},
            'user': {},
            '_user_common_base': {}, # last known common base user data between local and remote
            '_last_modified': None # timestamp of most recent modification (reset to None on each sync)
        }
        try:
            with open(get_cache_filename()) as file:
                try:
                    # Note: we are updating self._data with file content rather than overriding it
                    # to ensure inner _data keys always exist
                    self._data.update(json.load(file))
                except ValueError:
                    pass
        except (IOError, OSError) as ex:
            if ex.args[0] != 2:  # FileNotFoundError
                raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def save(self, force=False):
        """Persist local cache data to file if modified."""
        if self._data['_last_modified'] or force:
            makedirs(op.dirname(get_cache_filename()), exist_ok=True)
            tmp_filename = get_cache_filename() + '.tmp'
            with open(tmp_filename, 'w') as file:
                json.dump(self._data, file)
            shutil.move(tmp_filename, get_cache_filename())

    def get(self, level):
        """Returns local cache"""
        assert level in ('user', 'global'), 'Unsupported cache type: {}'.format(level)
        return self._data[level]

    def local_update(self, data):
        """Update when changes are made locally. This will trigger a push at the next opportunity."""
        self.update(data)
        with CacheTagsStore() as cache_tags:
            cache_tags.user_cache_tag = ''

    def update(self, data):
        """Partially update local user cache data"""
        validate_data(data)
        self._data['user'].update(data)
        self._data['_last_modified'] = timegm(datetime.utcnow().utctimetuple())

    def override(self, data):
        """Fully override local user cache data"""
        validate_data(data)
        self._data['user'] = data
        self._data['_last_modified'] = timegm(datetime.utcnow().utctimetuple())

    def delete_key(self, key):
        """Delete a local user cache key"""
        try:
            del self._data['user'][key]
            self._data['_last_modified'] = timegm(datetime.utcnow().utctimetuple())
        except KeyError:
            pass

    def merge_with(self, remote_global, remote_user):
        """Merge local cache with remote data"""

        # Validate remote data
        for step in [
            ('global', remote_global), ('user', remote_user)
        ]:
            level, data = step
            try:
                assert type(data) == dict, 'Must be of type dict'
                assert 'cache' in data.keys(), 'Missing \'cache\' field'
                assert 'meta' in data.keys(), 'Missing \'meta\' field'
                assert type(data.get('cache')) == dict, '\'cache\' field must be of type dict'
                assert type(data.get('meta')) == dict, '\'meta\' field must be of type dict'
                assert 'tag' in data.get('meta').keys(), 'Missing \'meta.tag\' field'
                assert 'timestamp' in data.get('meta').keys(), 'Missing \'meta.timestamp\' field'
            except AssertionError as ex:
                raise CacheErrorBadRemoteData('{} remote data: {}'.format(level, ex))

        # Merge global cache: server always wins
        self._data['global'] = remote_global['cache']

        # Merge user cache: if local is modified, prioritize local, else remote wins
        if self._data['_last_modified'] and remote_user['meta']['timestamp']:
            if self._data['_last_modified'] > int(remote_user['meta']['timestamp']):
                local_diff = diff(self._data['_user_common_base'], self._data['user'])
                self.override(patch(local_diff, remote_user['cache']))
            else:
                remote_diff = diff(self._data['_user_common_base'], remote_user['cache'])
                self.override(patch(remote_diff, self._data['user']))
        else:
            # Skip local cache, keep remote only
            self.override(remote_user['cache'])

        # Reset last known common base
        self._data['_user_common_base'] = self._data['user']

        # Reset the _last_modified timestamp key
        self._data['_last_modified'] = None

        # Persist new local cache to file
        self.save(force=True)


def validate_data(data):
    if type(data) is not dict:
        raise TypeError('Unsupported data type. Must be of type dict')

    for key, value in data.items():
        try:
            json.dumps(value)
        except TypeError:
            raise TypeError('\'{}\': Must be json serializable'.format(key))
