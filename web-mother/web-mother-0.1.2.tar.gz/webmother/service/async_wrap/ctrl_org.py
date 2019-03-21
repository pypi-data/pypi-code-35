# coding:utf-8

from webmother.service import ctrl_org
from asyncio import get_event_loop


async def create(oid, org_meta, *auth_args):
    args = (oid, org_meta, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_org.create, *args)


async def read(oid, *auth_args):
    args = (oid, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_org.read, *args)


async def update(oid, org_meta, *auth_args):
    args = oid, org_meta, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_org.update, *args)


async def change_status(oid, action, *auth_args):
    args = oid, action, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_org.change_status, *args)


async def children(oid, *auth_args):
    args = (oid, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_org.children, *args)


async def move(oid, oid_to, *auth_args):
    args = oid, oid_to, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_org.move, *args)


async def our_passports(oid, *auth_args):
    args = (oid, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_org.our_passports, *args)


async def app_activate(oid, *auth_args):
    args = (oid, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_org.app_activate, *args)


async def appid_deactivate(oid, *auth_args):
    args = oid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_org.appid_deactivate, *args)


async def vip_create(appid, level, display, *auth_args):
    args = appid, level, display, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_org.vip_create, *args)


async def vip_query(appid, *auth_args):
    args = appid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_org.vip_query, *args)
