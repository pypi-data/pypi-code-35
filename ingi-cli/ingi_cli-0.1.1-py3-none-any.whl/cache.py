"""
Let's make sure that any gists are cached and tracked locally as well. Gotta save
dat bandwidth.
"""

import datetime
import os
import pickledb
import shutil
import dateutil.parser

def get_default_cache_path():
    return os.path.join(os.path.expanduser("~"), '.ingi')


class Cache(pickledb.PickleDB):

    def __init__(self, cache_path=None, cache_index='index.db'):
        self.cache_path = cache_path
        if not cache_path:
            self.cache_path = get_default_cache_path()

        self.cache_index = cache_index

        cache_db_path = os.path.join(self.cache_path, cache_index)
        if not os.path.exists(self.cache_path):
            # folder and cache don't exist
            os.mkdir(self.cache_path)
        else:
            if not os.path.isdir(self.cache_path):
                raise Exception('The cache path exists as a file, `None` or directory expected.')

        super(Cache, self).__init__(cache_db_path, False, sig=True)

    def is_gist_cached(self, gist_id, is_newer=None):
        """
        Check cache for gist, check in cache index and then check physical file existence.
        :param gist_id: ID of the GitHub gist
        :param is_newer: A datetime object to check whether cache is newer than it.
        :returns: Cached object (dictionary) if exists otherwise False.
        """
        cached = self.get(gist_id)
        if not cached:
            return False
        else:
            if is_newer:
                naive = dateutil.parser.parse(cached['created_at']).replace(tzinfo=None)
                if naive < is_newer.replace(tzinfo=None):
                    return False
            
            try:
                # we open & close the file to check whether it exists and isn't corrupt.
                f = open(os.path.join(self.cache_path, cached['local_filepath'], cached['entrypoint']), 'r')
                f.close()
                return cached
            except FileNotFoundError:
                return False

    def load_gist_file_from_cache(self, gist):
        """
        """
        filepath = os.path.join(self.cache_path, gist['local_filepath'], gist['entrypoint'])
        try:
            # we open & close the file to check whether it exists and isn't corrupt.
            content = ''
            with open(filepath, 'r') as f:
                content = f.read()

            return content
        except:
            return None

    def cache_gist(self, gist_api_data, entrypoint):
        """
        Stores the gist file locally to be re-used.
        :param gist_api_data: The result gist json object from github API
        :param entrypoint: The script to invoke after gist is cached (required for gists with multiple files) 
        :returns: The dictionary that is cached.
        """
        gist_path = "gists/{user}/{gist_id}/{node_id}".format(user=gist_api_data['owner']['login'],
                                                                gist_id=gist_api_data['id'],
                                                                node_id=gist_api_data['node_id'])

        cache_data = {
            "id": gist_api_data['id'],
            "node_id": gist_api_data['node_id'],
            "created_at": gist_api_data['created_at'],
            "cached_at": datetime.datetime.utcnow().isoformat(),
            "files": {
                g['filename']: g['raw_url'] for g in gist_api_data['files'].values()
            },
            "author": gist_api_data['owner']['login'],
            "local_filepath": gist_path,
            "entrypoint": entrypoint,
            "language": gist_api_data['files'][entrypoint]['language']
        }
        self.set(gist_api_data['id'], cache_data)

        return cache_data

    @classmethod
    def clear(self, path=None):
        """
        Dump the cache index and remove all local gist files. This is a hard cache clear and 
        cannot be undone.
        """
        if not path:
            path = get_default_cache_path()
            
        if os.path.exists(path):
            shutil.rmtree(path)
        