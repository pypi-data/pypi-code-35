import json
from flask import request
from .route import Route
from .exceptions import AppNotDefined, HttpMethodConflict

class Froi(Route):
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
        self.method = []

    def route(self, url='', **kwargs):
        """Wrap server method's route"""
        add = self.app.add_url_rule
        add('{}{}'.format(self.prefix, url),
            methods=self.getmethods(),
            **kwargs)

        # handle forward slash
        if self.prefix is not '' or url is not '':
            add('{}{}/'.format(self.prefix, url),
                methods=self.getmethods(),
                **kwargs)

        self.method = []

    def install(self):
        """Attach routes to defined app"""
        self.setall().route(view_func=self.sethttp)

    def _check_methods(self, method):
        if method in self.method:
            raise HttpMethodConflict('Multiple {} in methods'.format(method))

        if self.method is not None:
            self.method += [method]
            return

        self.method = [method]

    def setall(self):
        self.method = ['GET', 'POST', 'PUT',
                       'DELETE', 'OPTIONS', 'HEADER']
        return self

    def setget(self):
        self._check_methods('GET')
        return self

    def setpost(self):
        self._check_methods('POST')
        return self

    def setput(self):
        self._check_methods('PUT')
        return self

    def setdelete(self):
        self._check_methods('DELETE')
        return self

    def setoptions(self):
        self._check_methods('OPTIONS')
        return self

    def setheader(self):
        self._check_methods('HEADER')
        return self
