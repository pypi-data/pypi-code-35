#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'demo_flask_restful'
__author__ = 'JieYuan'
__mtime__ = '19-3-1'
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, request

parser = reqparse.RequestParser()
parser.add_argument('args')  # 匹配需要的key


class Post(Resource):
    routing = '/post'

    def __init__(self):
        pass

    def get(self):
        dic = parser.parse_args()  # **dic
        return dic

    def post(self):
        """str(i, encoding='utf-8'): 字节转字符串
        application/json: request.form
        >> requests.post(url, data=[('key', 'value')])
        application/x-www-form-urlencoded: request.json
        >> requests.post(url, json={'key': 'value'})
        request.files: request.files['a']
        >> requests.post(url, files={'key':  open('./xx.txt')})
        """
        dic = request.json  # request.form
        return dic


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Post, Post.routing)
    app.run(debug=True)
