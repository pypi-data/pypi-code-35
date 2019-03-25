# -*- coding: utf-8 -*-
"""Модуль архиватора файлов и папок."""

import os
import subprocess

from msbackup import backend_base


class File(backend_base.Base):
    """Архиватор файлов и папок."""

    SECTION = 'Backend-File'

    def __init__(self, config, *args, **kwargs):
        """Конструктор."""
        super().__init__(config, *args, **kwargs)
        # config file options
        self.base_dir = kwargs.get('base_dir') or config.get(
            section=self.SECTION,
            option='BASE_DIR',
            fallback=None,
        )
        a_name = kwargs.get('archive_name') or config.get(
            section=self.SECTION,
            option='ARCHIVE_NAME',
            fallback=None,
        )
        self.archive_name = os.path.basename(a_name) if a_name else None

    def _archive(self, source, output, **kwargs):
        """
        Упаковка списка источников в файл архива.

        :param source: Список источников для архивации.
        :type source: [str]
        :param output: Путь к файлу с архивом.
        :type output: str
        """
        params = {
            'source': source,
            'output': output,
            'base_dir': kwargs.get('base_dir'),
        }
        ex = [os.path.dirname(output)]
        if self.exclude is not None:
            ex.extend(self.exclude)
        if 'exclude' in kwargs:
            ex.extend(kwargs['exclude'])
        params['exclude'] = ex
        if self.exclude_from is not None:
            exclude_from = []
            for exf in self.exclude_from:
                exclude_from.append(self._relative_to_abs(exf))
            params['exclude_from'] = exclude_from
        self.pack(**params)

    def _backup(self, sources=None, verbose=False, **kwargs):
        """
        Архивация файлов или папок.

        :param source: Список источников для архивации.
        :type source: [str]
        :param verbose: Выводить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """
        name = kwargs.get('archive_name', self.archive_name)
        if name is None:
            name = os.path.basename(sources[0])
        if name == '':
            name = os.uname().nodename
        output = self.outpath(name=name)
        base_dir = kwargs.get('base_dir', self.base_dir)
        if verbose:
            info = []
            for source in sources:
                if base_dir is None:
                    spath = source
                else:
                    spath = os.path.join(base_dir, source)
                if os.path.isfile(spath):
                    stype = 'file'
                else:
                    stype = 'directory'
                info.extend([stype, '|', source])
            self.out('Backup sources: ', *info)
        try:
            self.archive(
                source=sources,
                output=output,
                base_dir=base_dir,
                exclude=[self.backup_dir],
            )
        except subprocess.CalledProcessError as ex:
            if ex.stderr is not None:  # pragma: no coverage
                self.err(ex.stderr)
            return 1
        return 0
