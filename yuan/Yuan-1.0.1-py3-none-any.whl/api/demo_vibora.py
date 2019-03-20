# -*- coding: utf-8 -*-
"""
__title__ = 'vibora_test'
__author__ = 'JieYuan'
__mtime__ = '18-11-6'
"""
import jieba
import json
from vibora import Vibora, Request
from vibora.responses import JsonResponse
# from urllib import parse
# parse.unquote(parse.quote('中文'))

app = Vibora()


@app.route('/json', methods=['POST'])
async def home(request: Request):
    content = await request.stream.read()
    content = eval(content)
    content = jieba.lcut(content.get('text', ''))
    return JsonResponse(content)

# import requests
# r = requests.post('http://0.0.0.0:5000/json', json={'text': '小米公司还不错啊'})
# r.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, workers=4)
