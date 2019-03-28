import json
from app import douwa


def rpc_permission_verify(user):
    # from flask_douwa import redis

    if isinstance(user, dict):
        PERMISSION_PREFIX = "duowa:permission:"
        userrole = set(user["roles"])
        stri = '-'.join(userrole)
        key = "角色与权限"
        _str = '+'.join([stri, key])
        userrole_dd = douwa.permission_verify(data=_str, arg='permission')
        return userrole_dd

    elif isinstance(user, str):
        try:
            _user = json.loads(user)
        except Exception as e:
            _user = None
            raise Exception(e)
        if _user:
            PERMISSION_PREFIX = "duowa:permission:"
            userrole = set(_user["roles"])
            stri = '-'.join(userrole)
            key = "角色与权限"
            _str = '+'.join([stri, key])
            userrole_dd = douwa.permission_verify(data=_str, arg='permission')

            return userrole_dd