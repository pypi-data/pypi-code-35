# -*- coding: utf-8 -*-
"""Модуль архиватора репозиториев Mercurial."""

import os
import subprocess
import shutil

from msbackup.backend_base import Base as BaseBackend


def get_backend_kwargs(params):
    """Подготовка параметров для режима 'hg'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    BaseBackend.get_param(params, kwargs, 'repos_dir')
    BaseBackend.get_param(params, kwargs, 'hg_cmd')
    return kwargs


class Mercurial(BaseBackend):
    """Архиватор репозиториев системы контроля версий Mercurial."""

    SECTION = 'Backend-Mercurial'

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('hg')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        parser.add_argument(
            '-R', '--repos-dir', dest='repos_dir',
            help='Path to root of Mercurial repositories.')
        parser.add_argument(
            '--hg-cmd', dest='hg_cmd', help='Command to run mercurial util.')
        parser.add_argument(
            'source', nargs='*', metavar='REPO',
            help='Name of repository.')

    def __init__(self, config, **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        """
        super().__init__(config, **kwargs)
        # config file options
        self.hg_command = kwargs.get('hg_cmd') or config.get(
            section=self.SECTION,
            option='HG_COMMAND',
            fallback='/usr/bin/hg',
        )
        self.repos_dir = kwargs.get('repos_dir') or config.get(
            section=self.SECTION,
            option='REPOS_DIR',
            fallback=None,
        )
        # exclude_from
        if self.exclude_from is not None:
            exclude = self.exclude if self.exclude is not None else []
            for exf in self.exclude_from:
                exclude.extend(self._load_exclude_file(exf))
            self.exclude = exclude if len(exclude) > 0 else None
            self.exclude_from = None

    def _archive(self, source, output, **kwargs):
        """
        Архивация одного репозитория системы контроля версий Mercurial.

        :param source: Путь к репозиторию Mercurial.
        :type source: str
        :param output: Путь к файлу архива.
        :type output: str
        """
        name = os.path.basename(source)
        repo_bak = os.path.join(self.tmp_dir, name)
        try:
            subprocess.check_call(
                ['/usr/bin/hg', 'clone', '--noupdate', '--quiet',
                 source, repo_bak],
                stdout=self.stream_out,
                stderr=self.stream_err,
            )
            self.pack(
                source=name,
                output=output,
                base_dir=self.tmp_dir,
            )
        except Exception:
            raise
        finally:
            shutil.rmtree(repo_bak, ignore_errors=True)

    def _backup(self, sources=None, verbose=False, **kwargs):
        """
        Архивация всех репозиториев Mercurial в заданной папке.

        Если список имён репозиториев пуст, то архивируются все репозитории
        в папке REPOS_DIR.

        :param sources: Список имён репозиториев для архивации.
        :type sources: [str]
        :param verbose: Выодить информационные сообщения.
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
                if os.path.isdir(os.path.join(repo_path, '.hg')):
                    repos.append((name, repo_path))
        else:
            repos = self._scan_repos_dir(repos_dir)
        error_count = 0
        for repo, repo_path in repos:
            if verbose:
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
            if os.path.isdir(os.path.join(entry.path, '.hg')):
                repos.append((entry.name, entry.path))
        return repos
