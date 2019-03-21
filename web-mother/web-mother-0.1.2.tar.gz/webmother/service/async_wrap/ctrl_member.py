# coding:utf-8

from webmother.service import ctrl_member
from asyncio import get_event_loop


async def member_create(oid, indicator, identity_json, *auth_args):
    args = oid, indicator, identity_json, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_member.member_create, *args)


async def member_read(oid, uid, *auth_args):
    args = oid, uid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_member.member_read, *args)


async def member_update(oid, uid, mmb_meta, *auth_args):
    args = oid, uid, mmb_meta, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_member.member_update, *args)


async def member_remove(oid, uid, *auth_args):
    args = oid, uid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_member.member_remove, *args)


async def members_query(oid, *auth_args):
    args = (oid, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_member.members_query, *args)
