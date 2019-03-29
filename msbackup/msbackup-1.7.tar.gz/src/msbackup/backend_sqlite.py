# -*- coding: utf-8 -*-
"""Модуль архиватора баз данных SQLite."""

import os
import subprocess

from msbackup.backend_base import Base as BaseBackend


def get_backend_kwargs(params):
    """Подготовка параметров для режима 'sqlite'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    BaseBackend.get_param(params, kwargs, 'sqlite_cmd')
    return kwargs


class Sqlite(BaseBackend):
    """Архиватор баз данных SQLite."""

    SECTION = 'Backend-SQLite'

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('sqlite')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        parser.add_argument(
            '--sqlite-cmd',
            dest='sqlite_cmd',
            help='Command to run SQLite command-line shell.',
        )
        parser.add_argument(
            'source', nargs='*', metavar='DBNAME',
            help='Path to database file.')

    def __init__(self, config, *args, **kwargs):
        """Конструктор."""
        super().__init__(config, *args, **kwargs)
        self.suffix = '.gz' + (self.encryptor.suffix if self.encryptor else '')
        self.sqlite_cmd = kwargs.get('sqlite_cmd') or config.get(
            section=self.SECTION,
            option='SQLITE_COMMAND',
            fallback='/usr/bin/sqlite3',
        )

    def _archive(self, source, output, **kwargs):
        """
        Упаковка списка источников в файл архива.

        :param source: Путь к файлу БД SQLite.
        :type source: str
        :param output: Путь к файлу с архивом.
        :type output: str
        """
        bakdb = os.path.join(
            self.tmp_dir,
            os.path.basename(source),
        )
        try:
            subprocess.check_call(
                [self.sqlite_cmd,
                 source,
                 '.backup "{}"'.format(bakdb)],
                stdout=self.stream_out,
                stderr=self.stream_err,
            )
            with self.open(output, mode='wb') as out_file:
                with self.open(bakdb, mode='rb') as bakdb_file:
                    self._compress(in_stream=bakdb_file, out_stream=out_file)
        except Exception:
            raise
        finally:
            if os.path.exists(bakdb):
                os.remove(bakdb)

    def _backup(self, sources=None, verbose=False, **kwargs):
        """
        Архивация баз данных SQLite.

        :param source: Список источников для архивации.
        :type source: [str]
        :param verbose: Выводить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """
        error_count = 0
        for source in sources:
            output = self.outpath(os.path.basename(source))
            if verbose:
                self.out('Backup source: ', source)
            try:
                self.archive(
                    source=source,
                    output=output,
                )
            except subprocess.CalledProcessError as ex:
                if ex.stderr is not None:  # pragma: no coverage
                    self.err(ex.stderr)
                error_count += 1
        return error_count
