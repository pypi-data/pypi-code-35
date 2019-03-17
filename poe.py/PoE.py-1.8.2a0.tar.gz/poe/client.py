import urllib3

urllib3.disable_warnings()
import json

from poe.utils import strip_unicode
from urllib.parse import quote_plus

from .clientbase import ClientBase
from .exceptions import RequestException
from .exceptions import NotFoundException
from .exceptions import ServerException


class Client(ClientBase):
    def __init__(self, pool: urllib3.PoolManager = None):
        self.pool = pool or urllib3.PoolManager()
        self.base_url = "https://pathofexile.gamepedia.com/api.php?action=cargoquery"
    def request_gen(self, url, params=None):
        http = self.pool
        params['format'] = 'json'
        final_url = f"{url}"
        if 'where' in params:
            params['where'] = quote_plus(params['where'])
        if 'titles' in params:
            params['titles'] = quote_plus(params['titles'])
        for key, value in params.items():
            final_url = f"{final_url}&{key}={value.replace(' ', '%20')}"
        #print(final_url, params)
        try:
            r = http.request('GET', final_url)
        except:
            return print(final_url, params)
        # print(final_url)
        try:
            resp = json.loads(r.data.decode('utf-8'))
        except (urllib3.exceptions.TimeoutError, urllib3.exceptions.ConnectionError):
            raise RequestException(r, {})

        if 300 > r.status >= 200:
            return resp
        elif r.status == 404:
            raise NotFoundException(r, resp)
        elif r.status > 500:
            raise ServerException(r, resp)
        else:
            raise RequestException(r, resp)

    def find_items(self, where: dict, limit=None):
        params = self.item_param_gen(where, limit)
        data = self.request_gen(self.base_url, params=params)
        return self.item_list_gen(data, self.request_gen, self.base_url, where)

    def find_gems(self, where: dict):
        return self.get_gems(where, self.request_gen, self.base_url)

    def search(self, name: str):
        search_params = {
            'tables': 'skill, items',
            'join_on': 'skill._pageName=items._pageName',
            'fields': 'items._pageName=name,tags',
            'where': f'name%20LIKE%20%22{name}%%22'
        }
        results = self.extract_cargoquery(self.request_gen(self.base_url, params=search_params))
        fetched_results = []
        print(results)
        for result in results:
            if 'gem' in result['tags']:
                fetched_results.append(self.get_gems({'name': f'{result["name"]}'})[0])
            elif any(i_type in result['tags'] for i_type in ['ring', 'amulet', 'belt', 'armour']):
                fetched_results.append(self.get_items({'name': f'{name}%'})[0])
        return fetched_results
