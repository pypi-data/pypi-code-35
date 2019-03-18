#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'sanic'
__author__ = 'JieYuan'
__mtime__ = '19-3-1'
"""

from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route('/get')
async def get(request):
    return json(request.args)


@app.route('/post', methods=['POST'])
async def post(request):
    return json(request.json)


# def test():
#     import requests
#     r = requests.get('http://0.0.0.0:8000/get', params={'a': 1})
#     r.json()
#     # {'a': ['1']}
#
#     r = requests.post('http://0.0.0.0:8000/post', json={'a': 1})
#     r.json()
#     # {'a': 1}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
