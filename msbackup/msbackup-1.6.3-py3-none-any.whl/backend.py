# -*- coding: utf-8 -*-
"""Модуль архиваторов."""

from msbackup.backend_file import File
from msbackup.backend_svn import Subversion
from msbackup.backend_hg import Mercurial
from msbackup.backend_pg import PostgreSQL
from msbackup.backend_sqlite import Sqlite


BACKENDS = {
    'file': File,
    'svn': Subversion,
    'hg': Mercurial,
    'pg': PostgreSQL,
    'sqlite': Sqlite,
}


def make_backend(name, *args, **kwargs):
    """
    Создание объекта архиватора.

    :param name: Имя архиватора.
    :type name: str
    :param config: Объект конфигурации архиватора.
    :type config: :class:`ConfigParser.RawConfigParser`
    """
    if name not in BACKENDS:
        raise Exception('Unknown back-end: {}'.format(name))
    return BACKENDS[name](*args, **kwargs)
