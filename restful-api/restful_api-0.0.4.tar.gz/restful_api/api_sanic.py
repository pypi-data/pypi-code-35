#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'api_sanic'
__author__ = 'JieYuan'
__mtime__ = '19-3-4'
"""

import socket

socket.SO_REUSEPORT = 15

from collections import OrderedDict

from vibora import Vibora, Request
from vibora.responses import JsonResponse

from sanic import Sanic
from sanic.response import json


class Api(object):

    def __init__(self, routing, predict, app=Sanic(), app_type='sanic', verbose=True):
        """
        :param predict:
            def func(*args):
                pass
                :return score
        """
        self.app = app
        self.predict = predict
        self.app.route(routing, methods=['GET', 'POST'])(self.__getattribute__(f'post_{app_type}'))
        self.verbose = verbose

    async def post_sanic(self, request):
        input = request.json
        output = OrderedDict()

        try:
            output['Score'] = self.predict(**input)
        except Exception as e:
            output['Predict error'] = str(e)
            output['Score'] = 0
        finally:
            if self.verbose:
                output['Requestion'] = input

        return json(output)

    async def post_vibora(self, request: Request):
        input = await request.stream.read()
        output = OrderedDict()

        try:
            input = eval(input)
        except Exception as e:
            output['Input error'] = str(e)

        try:
            output['Score'] = self.predict(**input)
        except Exception as e:
            output['Predict error'] = str(e)
            output['Score'] = 0
        finally:
            if self.verbose:
                output['Requestion'] = input

        return JsonResponse(output)


if __name__ == '__main__':
    import jieba

    pred1 = lambda **kwargs: kwargs['x'] + kwargs['y']
    pred2 = lambda x=1, y=1: x - y
    pred3 = lambda text='小米是家不错的公司': jieba.lcut(text)

    api = Api('/post1', pred1)
    api = Api('/post2', pred2, app=api.app)
    api = Api('/post3', pred3, app=api.app)
    api.app.run('0.0.0.0')
