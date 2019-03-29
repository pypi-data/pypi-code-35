# -*- coding: utf-8 -*-
"""Модуль архиватора репозиториев Subversion."""

import os
import subprocess
import shutil

from msbackup.backend_base import Base as BaseBackend


def get_backend_kwargs(params):
    """Подготовка параметров для режима 'svn'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    BaseBackend.get_param(params, kwargs, 'repos_dir')
    BaseBackend.get_param(params, kwargs, 'svnadmin_cmd')
    return kwargs


class Subversion(BaseBackend):
    """Архиватор репозиториев системы контроля версий Subversion."""

    SECTION = 'Backend-Subversion'

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('svn')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        parser.add_argument(
            '-R', '--repos-dir',
            help='Path to root of Subversion repositories.',
        )
        parser.add_argument(
            '--svnadmin-cmd',
            help='Command to run svnadmin util (default: /usr/bin/svnadmin).',
        )
        parser.add_argument(
            'source', nargs='*', metavar='REPO',
            help='Name of repository.',
        )

    def __init__(self, config, **kwargs):
        """Конструктор."""
        super().__init__(config, **kwargs)
        # config file options
        self.repos_dir = kwargs.get('repos_dir') or config.get(
            section=self.SECTION,
            option='REPOS_DIR',
            fallback=None,
        )
        self.svnadmin_cmd = kwargs.get('svnadmin_cmd') or config.get(
            section=self.SECTION,
            option='SVNADMIN_COMMAND',
            fallback='/usr/bin/svnadmin',
        )
        # exclude_from
        if self.exclude_from is not None:
            exclude = self.exclude if self.exclude is not None else []
            for exf in self.exclude_from:
                exclude.extend(self._load_exclude_file(exf))
            self.exclude = exclude if len(exclude) > 0 else None
            self.exclude_from = None

    def outpath(self, name, **kwargs):
        """
        Формирование имени файла с архивом.

        :param name: Имя архива без расширения.
        :type name: str
        :return: Полный путь к файлу архива.
        :rtype: str
        """
        fname = name + '.svn' + self.compressor_suffix
        if self.encryptor is not None:
            fname += self.encryptor.suffix
        return os.path.join(self.backup_dir, fname)

    def _archive(self, source, output, **kwargs):
        """
        Архивация одного репозитория системы контроля версий Subversion.

        :param source: Путь к репозиторию Subversion.
        :type source: str
        :param output: Путь к файлу с архивом.
        :type output: str
        """
        repo_copy = os.path.join(self.tmp_dir, os.path.basename(source))
        try:
            subprocess.check_call(
                [self.svnadmin_cmd, 'hotcopy', '--clean-logs',
                 source, repo_copy],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
            p1 = subprocess.Popen(
                [self.svnadmin_cmd, 'dump', '--quiet', '--deltas', repo_copy],
                stdout=subprocess.PIPE,
            )
            with self.open(output, 'wb') as out:
                self._compress(in_stream=p1.stdout, out_stream=out)
        except Exception:
            raise
        finally:
            shutil.rmtree(repo_copy, ignore_errors=True)

    def _backup(self, sources=None, verbose=False, **kwargs):
        """
        Архивация всех репозиториев Subversion, находящихся в заданной папке.

        Если список sources руст, то выполняется сканирование папки REPOS_DIR.

        :param sources: Список имён репозиториев.
        :type sources: [str]
        :param verbose: Выводить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """
        repos_dir = kwargs.get('repos_dir', self.repos_dir)
        if sources:
            repos = []  # Список имён и путей к репозиториям для архивации.
            for name in sources:
                repo_path = os.path.join(repos_dir, name)
                if not os.path.isdir(repo_path):
                    continue
                if os.path.isfile(os.path.join(repo_path, 'format')):
                    repos.append((name, repo_path))
        else:
            repos = self._scan_repos_dir(repos_dir)
        error_count = 0
        for repo, repo_path in repos:
            if verbose is True:
                self.out('Backup repo: ', repo)
            try:
                self.archive(
                    source=repo_path,
                    output=self.outpath(name=repo),
                )
            except subprocess.CalledProcessError as ex:
                error_count += 1
                self.err(ex.stderr)
        return error_count

    def _scan_repos_dir(self, repos_dir):
        """Сканирование папки с репозиториями."""
        repos = []  # Список имён и путей к репозиториям для архивации.
        for entry in os.scandir(repos_dir):
            if self.exclude is not None and entry.name in self.exclude:
                continue
            if not entry.is_dir():
                continue
            if os.path.isfile(os.path.join(entry.path, 'format')):
                repos.append((entry.name, entry.path))
        return repos
