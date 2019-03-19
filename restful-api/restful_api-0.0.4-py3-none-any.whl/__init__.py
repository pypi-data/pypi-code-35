#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'api_sanic'
__author__ = 'JieYuan'
__mtime__ = '19-3-4'
"""

__version__ = '0.0.4'
# import socket
#
# socket.SO_REUSEPORT = 15
# from vibora import Vibora, Request
# from vibora.responses import JsonResponse
from sanic import Sanic
from sanic.response import json

from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html
from collections import OrderedDict


class Api(object):

    def __init__(self, routing, predict, app=Sanic(), method='POST', verbose=True, version=''):
        """
        :param predict:
            def func(*args):
                pass
                :return score
        """

        self.app = app
        self.method = method
        self.predict = predict
        self.version = version
        self.verbose = verbose

        self.app_type = app.__repr__().split('.')[0][1:]
        self.app.route(routing, methods=['GET', 'POST'])(self.__getattribute__(self.app_type))

    async def sanic(self, request):
        """
        request.json: {'a': 1}
        request.args:  {'a': ['1']}
        """
        input = request.json if self.method == 'POST' else request.args
        output = OrderedDict()
        if self.version:
            output['Version'] = self.version
        try:
            output['prob'] = output['Score'] = self.predict(**input)
        except Exception as e:
            error = format_exc().strip()
            output['Predict error'] = error  # str(e)
            output['prob'] = output['Score'] = 0
            print(error)
        finally:
            if self.verbose:
                output['Request'] = input

        return json(output)

    # async def vibora(self, request: Request):
    #     input = await request.stream.read()
    #     output = OrderedDict()
    #
    #     try:
    #         input = eval(input)
    #     except Exception as e:
    #         output['Input error'] = format_exc() # str(e)
    #
    #     try:
    #         output['Score'] = self.predict(**input)
    #     except Exception as e:
    #         output['Predict error'] = format_exc() # str(e)
    #         output['Score'] = 0
    #     finally:
    #         if self.verbose:
    #             output['Requestion'] = input
    #
    #     return JsonResponse(output)


if __name__ == '__main__':
    import jieba

    pred1 = lambda **kwargs: kwargs['x'] + kwargs['y']
    pred2 = lambda x=1, y=1: x - y
    pred3 = lambda text='小米是家不错的公司': jieba.lcut(text)
    pred4 = lambda **kwargs: kwargs

    api = Api('/post1', pred1, app=Sanic())
    api = Api('/post2', pred2, app=api.app)
    api = Api('/post3', pred3, app=api.app)
    api = Api('/getgo', pred4, app=api.app, method='GET', version=666)
    api.app.run(debug=True)
