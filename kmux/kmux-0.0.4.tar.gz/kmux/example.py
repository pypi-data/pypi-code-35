# -*- coding:utf-8 -*-

from kmux.rest import KmuxHandler, REST, GET, POST, Kmux
from kmux.rest import Int32Field


class ExampleHandler(KmuxHandler):
    __KMUX_PATH_PREFIX__ = '/api/v1'

    def is_debug_mode(self):
        return True


@REST
class WelcomeHandler1(ExampleHandler):
    @GET('/hello')
    def hello(self):
        self.set_response({
            'message': 'hello world'
        })


@REST
class WelcomeHandler2(ExampleHandler):
    @GET('/add', params=dict(
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
