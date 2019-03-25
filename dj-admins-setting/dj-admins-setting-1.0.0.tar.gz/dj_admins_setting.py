# -*- coding: utf-8 -*-

import os
from email.utils import getaddresses


DEFAULT_ENV = 'ADMINS'


def config(env=DEFAULT_ENV, default=None):
    """Returns a valid ADMINS tuple list."""

    admins = []

    s = os.environ.get(env, default)

    if s:
        admins = parse(s)

    return admins


def parse(emails):
    """Parses an email string."""

    return getaddresses([emails])
