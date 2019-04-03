from drongo.utils.endpoint import APIEndpoint
from drongo.utils.helpers import URLHelper


class NamespaceCreate(APIEndpoint):
    __url__ = '/ns'
    __http_methods__ = ['POST']

    def init(self):
        self.obj = self.ctx.request.json
        self.ns_svc = self.ctx.modules.ns.services

    def call(self):
        svc = self.ns_svc.NamespaceCreate(**self.obj)
        return svc.call(ns=self.ctx.ns).json()


class NamespaceGet(APIEndpoint):
    __url__ = '/ns/{_id}'
    __http_methods__ = ['GET']

    def init(self):
        self.ns_svc = self.ctx.modules.ns.services

    def call(self):
        svc = self.ns_svc.NamespaceGet(uid=self._id)
        ns = svc.call(ns=self.ctx.ns)
        if ns is not None:
            return ns.json()


class NamespaceActivate(APIEndpoint):
    __url__ = '/ns/{_id}/operations/activate'
    __http_methods__ = ['GET', 'POST']

    def init(self):
        self.ns_svc = self.ctx.modules.ns.services

    def call(self):
        svc = self.ns_svc.NamespaceActivate(uid=self._id)
        svc.call(ns=self.ctx.ns)
        return 'OK'


class NamespaceDeactivate(APIEndpoint):
    __url__ = '/ns/{_id}/operations/deactivate'
    __http_methods__ = ['GET', 'POST']

    def init(self):
        self.ns_svc = self.ctx.modules.ns.services

    def call(self):
        svc = self.ns_svc.NamespaceDeactivate(uid=self._id)
        svc.call(ns=self.ctx.ns)
        return 'OK'


class NamespaceUpdate(APIEndpoint):
    __url__ = '/ns/{_id}'
    __http_methods__ = ['PUT']

    def init(self):
        self.obj = self.ctx.request.json
        self.ns_svc = self.ctx.modules.ns.services

    def call(self):
        svc = self.ns_svc.NamespaceUpdate(
            uid=self._id,
            name=self.obj.get('name'),
            description=self.obj.get('description')
        )
        svc.call(ns=self.ctx.ns)
        return 'OK'


class NamespaceDelete(APIEndpoint):
    __url__ = '/ns/{_id}'
    __http_methods__ = ['DELETE']

    def init(self):
        self.ns_svc = self.ctx.modules.ns.services

    def call(self):
        svc = self.ns_svc.NamespaceDelete(uid=self._id)
        svc.call(ns=self.ctx.ns)
        return 'OK'


class NamespaceList(APIEndpoint):
    __url__ = '/ns'
    __http_methods__ = ['GET']

    def init(self):
        q = self.ctx.request.query
        self.active_only = q.get('active_only', ['yes'])[0] == 'yes'
        self.page_number = int(q.get('page_number', [1])[0])
        self.page_size = int(q.get('page_size', [50])[0])
        self.ns_svc = self.ctx.modules.ns.services

    def call(self):
        svc = self.ns_svc.NamespaceList(
            active_only=self.active_only,
            page_number=self.page_number,
            page_size=self.page_size
        )
        count, items = svc.call(ns=self.ctx.ns)
        return {
            'count': count,
            'items': list(map(
                lambda item: item.json(),
                items
            ))
        }


AVAILABLE_API = [
    NamespaceCreate,
    NamespaceGet,
    NamespaceActivate,
    NamespaceDeactivate,
    NamespaceUpdate,
    NamespaceDelete,
    NamespaceList
]


class NamespaceAPI(object):
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
                base_url=self.base_url)
