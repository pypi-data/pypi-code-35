# -*- coding: utf-8 -*-
"""Модуль архиватора баз данных SQLite."""

import os
import subprocess

from msbackup import backend_base


class Sqlite(backend_base.Base):
    """Архиватор баз данных SQLite."""

    SECTION = 'Backend-SQLite'

    def __init__(self, config, *args, **kwargs):
        """Конструктор."""
        super().__init__(config, *args, **kwargs)
        self.suffix = '.gz' + (self.encryptor.suffix if self.encryptor else '')
        self.sqlite_cmd = config.get(
            section=self.SECTION,
            option='SQLITE_COMMAND',
            fallback='/usr/bin/sqlite3',
        )
        self.compress_level = config.getint(
            section=self.SECTION,
            option='COMPRESS_LEVEL',
            fallback=9,
        )

    def _archive(self, source, output, **kwargs):
        """
        Упаковка списка источников в файл архива.

        :param source: Список источников для архивации.
        :type source: [str]
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
            with self.open(output, mode='wb') as out:
                subprocess.check_call(
                    ['/bin/gzip',
                     '--stdout',
                     '-{}'.format(self.compress_level),
                     bakdb],
                    stdout=out,
                    stderr=self.stream_err,
                )
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
