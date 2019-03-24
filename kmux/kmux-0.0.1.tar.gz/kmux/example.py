# -*- coding:utf-8 -*-

from rest import KmuxHandler, REST, GET, POST, Kmux
from rest import Int32Field


Kmux.load_apis('example-apis.json')


class ExampleHandler(KmuxHandler):
    __KMUX_PATH_PREFIX__ = '/api'

    def is_debug_mode(self):
        return True


@REST
class WelcomeHandler1(ExampleHandler):
    @GET('/')
    def hello(self):
        self.set_response({
            'message': 'hello world'
        })


@REST
class WelcomeHandler2(ExampleHandler):
    @POST('/add', params=dict(
        x=Int32Field(required=True),
        y=Int32Field(required=True),
    ))
    def add(self, params):
        x = params['x']
        y = params['y']
        z = x + y
        self.set_response({
            'result': z
        })
