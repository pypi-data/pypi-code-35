#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
# Author: yuyongpeng@hotmail.com
# Description:
#  

"""

from wechatpy import WeChatClient
from redis import Redis
from wechatpy.session.redisstorage import RedisStorage
from wechatpy.exceptions import WeChatClientException

app_id = 'wx9af3e63ca6cc792c'
secret = 'f4d4661134a9694f9ebf1a60c8742007'
user_id = 'oGdq9s0W1DYA1TbMIH2tXPCiz3aA'
client = WeChatClient(app_id, secret)
print(client.access_token)
user = client.user.get(user_id)
# menu = client.menu.get()
redis_client = Redis.from_url('redis://127.0.0.1:6379/0')
session_interface = RedisStorage(
    redis_client,
    prefix="wechatpy"
)

wechat_client = WeChatClient(
    app_id,
    secret,
    session=session_interface
)



client.message.send_text(user_id, 'content')
try:
    res = wechat_client.user.get('oGdq9s0W1DYA1TbMIH2tXPCiz3aa')
    print(res)
except WeChatClientException as e:
    print(e)
    print(e.errcode)
# 以此类推，参见下面的 API 说明
# client.media.xxx()
# client.group.xxx()






























