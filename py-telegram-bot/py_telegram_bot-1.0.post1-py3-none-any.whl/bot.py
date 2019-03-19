from requests import Session
from .uploader import TelegramUploader
from .exceptions import TelegramAPIException


class DotDict(dict):
    def __getattr__(self, item):
        if isinstance(self[item], dict):
            return DotDict(self[item])
        else:
            return self[item]


class Bot:
    def __init__(self, token, proxy_type=None, proxy_url=None):
        self.token = token
        self.url = f'https://api.telegram.org/bot' + token
        self.session = Session()
        if proxy_type and proxy_url:
            if proxy_type.lower() == 'socks5':
                proxy = 'socks5://' + proxy_url
            elif proxy_type.lower() == 'http' or proxy_type.lower() == 'https':
                proxy = proxy_url
            else:
                raise TelegramAPIException('Unknown proxy type! Currently supported SOCKS5 and HTTP/HTTPS')
            self.session.proxies = {'http': proxy, 'https': proxy}

    def get_updates(self):
        offset = 0
        while True:
            try:
                r = self.session.get(self.url + '/getUpdates', params={'offset': offset}).json()
                if r['result']:
                    for res in r['result']:
                        if 'message' in res:
                            yield DotDict(res['message'])
                    offset = r['result'][-1]['update_id'] + 1
            except KeyboardInterrupt:
                break

    def get_api(self):
        return TelegramMethod(self, '')

    def get_uploader(self):
        return TelegramUploader(self)


class TelegramMethod:
    def __init__(self, bot, name):
        self.name = name
        self.bot = bot

    def __getattr__(self, method):
        if '_' in method:
            method = method.split('_')
            method = method[0] + ''.join(m.title() for m in method[1:])

        return TelegramMethod(self.bot, method)

    def __call__(self, **kwargs):
        r = self.bot.session.get(self.bot.url + '/' + self.name, params=kwargs).json()
        if not r['ok']:
            raise TelegramAPIException(r['description'])
        else:
            return r
