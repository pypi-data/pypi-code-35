# coding:utf-8

from webmother.service import ctrl_mine
from asyncio import get_event_loop


async def query_identities(appid, uid, access_token, member_type=0):
    args = appid, uid, access_token, member_type
    return await get_event_loop().run_in_executor(None, ctrl_mine.query_identities, *args)


async def get_vip_identity(appid, uid, access_token):
    args = appid, uid, access_token
    return await get_event_loop().run_in_executor(None, ctrl_mine.get_vip_identity, *args)
