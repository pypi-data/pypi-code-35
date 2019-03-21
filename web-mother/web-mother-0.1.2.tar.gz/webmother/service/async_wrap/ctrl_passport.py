# coding:utf-8

from webmother.service import ctrl_passport
from asyncio import get_event_loop


async def get_passport_tpl(cid, *auth_args):
    args = cid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_passport.get_passport_tpl, *args)


async def passport_create(cid, oid, passport_json, *auth_args):
    args = cid, oid, passport_json, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_passport.passport_create, *args)


async def passport_read(cid, oid, *auth_args):
    args = cid, oid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_passport.passport_read, *args)


async def passport_update(cid, oid, passport_json, *auth_args):
    args = cid, oid, passport_json, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_passport.passport_update, *args)


async def passport_remove(cid, oid, *auth_args):
    args = cid, oid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_passport.passport_remove, *args)


async def passports_query(cid, *auth_args):
    args = (cid, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_passport.passports_query, *args)
