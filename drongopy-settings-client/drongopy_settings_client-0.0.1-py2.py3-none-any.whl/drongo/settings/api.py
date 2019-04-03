from drongo.utils.endpoint import APIEndpoint
from drongo.utils.helpers import URLHelper


class SettingsSet(APIEndpoint):
    __url__ = '/settings/{module}'
    __http_methods__ = ['PUT']

    def init(self):
        self.obj = self.ctx.request.json
        self.set_svc = self.ctx.modules.settings.services

    def call(self):
        svc = self.set_svc.SettingsSet(
            mod=self.module, settings=self.obj)
        svc.call()


class SettingsGet(APIEndpoint):
    __url__ = '/settings/{module}'
    __http_methods__ = ['GET']

    def init(self):
        self.set_svc = self.ctx.modules.settings.services

    def call(self):
        svc = self.set_svc.SettingsGet(mod=self.module)
        res = svc.call()
        if res is not None:
            return res.json()


AVAILABLE_API = [
    SettingsSet, SettingsGet
]


class SettingsAPI(object):
    def __init__(self, app, module, base_url):
        self.app = app
        self.module = module
        self.base_url = base_url

        self.init_endpoints()

    def init_endpoints(self):
        for endpoint in AVAILABLE_API:
            URLHelper.endpoint(
                app=self.app,
                klass=endpoint,
                base_url=self.base_url
            )
