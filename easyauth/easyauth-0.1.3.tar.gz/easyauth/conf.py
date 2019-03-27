# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN = "USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN"
ACCOUNT_LOGOUT_ON_GET = "ACCOUNT_LOGOUT_ON_GET"
DISABLE_REGISTER = "DISABLE_REGISTER"
LANG_PARAM = "LANG_PARAM"

__DEFAULT_CONFIG = {
    USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN: "123456",
    ACCOUNT_LOGOUT_ON_GET: False,
    DISABLE_REGISTER: False,
    LANG_PARAM: "lang",
}


def __load_conf():
    return getattr(settings, 'EASYAUTH_CONF', __DEFAULT_CONFIG)


def get_conf(key, default_value=None):
    conf_dict = __load_conf()
    use_default = default_value
    if use_default is None:
        use_default = __DEFAULT_CONFIG.get(key, None)
    return conf_dict.get(key, use_default)


def is_debug_enabled():
    return getattr(settings, 'DEBUG', False)
