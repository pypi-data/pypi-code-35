import json

class AppNotDefined(Exception):
    """All routes will fail if app is not defined"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class HttpMethodConflict(Exception):
    """Defined HTTP methods with defined function once"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Froi:
    """
    Template for all routes to be created for APIs.

    A Flask wrapper that installs routes as defined from a class.
    It will accept :app: as paremeter that will be the server's
    context and will be used to set route.
    """

    def __init__(self, app, component_name, prefix=''):
        self.component_name = component_name
        self.prefix = prefix
        if app.add_url_rule is None:
            raise AppNotDefined('Sent `app` is not valid')

        self.app = app
        self.method = None

    def route(self, url='', **kwargs):
        """Wrap server method's route"""
        add = self.app.add_url_rule
        add('{}{}'.format(self.prefix, url),
            methods=self.method,
            **kwargs)

        # handle forward slash
        if self.prefix is not '' or url is not '':
            add('{}{}/'.format(self.prefix, url),
                methods=self.method,
                **kwargs)

        self.method = None

    def _master_fxn(self, **kwargs):
        from flask import request
        return json.dumps({
            'message': '{} on {}'.format(request.method, self.component_name)
        })

    def install(self):
        """Attach routes to defined app"""
        self.all().route(view_func=self._master_fxn)

    def _check_methods(self, method):
        if self.method is not None:
            self.method += [method]
            return

        self.method = [method]

    def all(self):
        self.get().post().put().delete()
        return self

    def get(self):
        self._check_methods('GET')
        return self

    def post(self):
        self._check_methods('POST')
        return self

    def put(self):
        self._check_methods('PUT')
        return self

    def delete(self):
        self._check_methods('DELETE')
        return self
