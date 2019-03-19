# -*- coding: utf-8 -*-
"""Archivers module."""

import os
import shutil
import stat
import subprocess


class Tar(object):
    """Архиватор посредством утилиты tar."""

    SECTION = 'Archive-Tar'

    def __init__(self, config, encryptor=None):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param encryptor: Шифровальщик архива.
        """
        self.cmd = config.get(self.SECTION, 'COMMAND', fallback='/bin/tar')
        self.params = config.get(
            self.SECTION,
            'ARCHIVER_PARAMS',
            fallback='--gzip',
        ).split(' ')
        self.suffix = config.get(self.SECTION, 'SUFFIX', fallback='.tar.gz')
        self.progress_suffix = config.get(
            self.SECTION,
            'PROGRESS_SUFFIX',
            fallback='.in_progress',
        )
        self.encryptor = encryptor

    def pack(self, source, output=None, base_dir=None, **kwargs):
        """
        Архивация файлов или папки.

        :param source: Источник или список источников для архивации.
        :type source: str или [str]
        :param output: Путь к файлу архива.
        :type output: str
        :param base_dir: Путь к папке с архивами.
        :type base_dir: str
        :param kwargs: Дополнительные параметры для tar.
        :type kwargs: [str]
        """
        sources = [source] if isinstance(source, str) else source
        if output is None:
            src = sources[0]
            if base_dir is None:
                output = src + self.suffix
            else:
                output = os.path.join(base_dir, src + self.suffix)
        tmp_path = output + self.progress_suffix
        params = ['/bin/tar', '--create', '--file', tmp_path]
        params.extend(self.params)
        if base_dir is not None:
            params.extend(['-C', base_dir])
        if 'exclude' in kwargs:
            for ex in kwargs['exclude']:
                params.append('--exclude={}'.format(ex))
        if 'exclude_from' in kwargs:
            for exf in kwargs['exclude_from']:
                params.append('--exclude-from={}'.format(exf))
        params.extend(sources)
        subprocess.run(
            params,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=True,
        )
        if self.encryptor is not None:
            try:
                self.encryptor.encrypt(tmp_path, output)
            except subprocess.CalledProcessError:
                raise
            finally:
                os.remove(tmp_path)
        else:
            shutil.move(tmp_path, output)


ARCHIVERS = {'tar': Tar}


def make_archiver(name, *args, **kwargs):
    """
    Фабрика архиватора.

    :param name: Имя архиватора.
    :type name: str
    :param config: Конфигурация.
    :type config: :class:`ConfigParser.RawConfigParser`
    :param encryptor: Шифровальщик.
    """
    if name not in ARCHIVERS:
        raise Exception('Unknown archiver: {}'.format(name))
    return ARCHIVERS[name](*args, **kwargs)
