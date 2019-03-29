# -*- coding: utf-8 -*-
"""Модуль базового класса всех архиваторов."""

import os
import tempfile
import stat
import sys
import glob
import shutil
import getpass
import subprocess
import abc

from msbackup import utils, archive, encrypt


class Base(metaclass=abc.ABCMeta):
    """Базовый класс архиваторов."""

    BACKUP_DIR_PERMISSIONS = (
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP |
        stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    )
    ARCHIVE_PERMISSIONS = (
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP
    )

    @classmethod
    def get_param(cls, params, kwargs, name):
        """Извлечение параметра из объекта."""
        value = getattr(params, name)
        if value is not None:
            kwargs[name] = value

    @classmethod
    def get_common_backend_kwargs(cls, params):
        """Извлечение общих параметров конструктора движка."""
        kwargs = {}
        cls.get_param(params, kwargs, 'backup_dir')
        cls.get_param(params, kwargs, 'tmp_dir')
        cls.get_param(params, kwargs, 'rotate')
        cls.get_param(params, kwargs, 'archiver')
        cls.get_param(params, kwargs, 'encryptor')
        cls.get_param(params, kwargs, 'exclude')
        cls.get_param(params, kwargs, 'exclude_from')
        cls.get_param(params, kwargs, 'compressor_cmd')
        cls.get_param(params, kwargs, 'tar_cmd')
        cls.get_param(params, kwargs, 'gpg_cmd')
        cls.get_param(params, kwargs, 'gpg_recipient')
        return kwargs

    @classmethod
    def make_options(cls, parser, version):
        """Добавление параметров командной строки."""
        archivers = sorted([item for item in archive.ARCHIVERS])
        encryptors = sorted([item for item in encrypt.ENCRYPTORS])
        parser.add_argument(
            '-c', '--config', metavar='FILE',
            help='Path to config file.',
        )
        parser.add_argument(
            '-b', '--backup-dir', dest='backup_dir',
            help='Path to archive directory (current by default).',
        )
        parser.add_argument(
            '-t', '--tmp-dir',
            help='Folder path for temporary files.'
        )
        parser.add_argument(
            '-a', '--archiver', choices=archivers,
            help='Name of file archiver.',
        )
        parser.add_argument(
            '-E', '--encryptor', choices=encryptors,
            help='Name of file encryptor.',
        )
        parser.add_argument(
            '-x', '--exclude', action='append', metavar='PATTERN',
            help='Exclude files defined by the PATTERN.',
        )
        parser.add_argument(
            '-X', '--exclude-from', dest='exclude_from',
            action='append', metavar='FILE',
            help='Exclude files defined in FILE.',
        )
        parser.add_argument(
            '-r', '--rotate', type=int,
            help='Number of archive files to be rotated.',
        )
        parser.add_argument(
            '-C', '--compressor-cmd',
            help='Command to run compressor (default: /bin/gzip -q9).',
        )
        parser.add_argument(
            '-T', '--tar-cmd',
            help='Command to run tar (default: /bin/tar --gzip).',
        )
        parser.add_argument(
            '-G', '--gpg-cmd',
            help='Command to run gnupg (default: /usr/bin/gpg).',
        )
        parser.add_argument(
            '-R', '--gpg-recipient',
            help='The recipient of the encrypted archive.',
        )
        parser.add_argument(
            '-v', '--verbose', action='store_true',
            help='Verbose output.',
        )
        parser.add_argument(
            '-d', '--debug', action='store_true',
            help='Print traceback when errors occured.',
        )
        parser.add_argument(
            '-V', '--version', action='version',
            version=version,
        )
        return parser.add_subparsers(
            dest='backend',
            title='Back-end name',
        )

    @classmethod
    def validate_params(cls, parser, params):
        """Проверка параметров."""
        if params.backend is None:
            parser.error(
                'the following arguments are required: Back-end')

    def __init__(self, config, **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        """
        self.encoding = sys.getdefaultencoding()
        # Config
        if hasattr(config, 'config_file_path'):
            self.config_file_dir = os.path.dirname(
                getattr(config, 'config_file_path'))
        else:
            self.config_file_dir = None
        self.stream_out = kwargs.get('out') or sys.stdout
        self.stream_err = kwargs.get('err') or sys.stderr
        # OPTIONS
        backup_user = config.get(self.SECTION, 'BACKUP_USER', fallback=None)
        if backup_user is not None:
            if getpass.getuser() != backup_user:
                raise Exception('This program must be run as {}. '
                                'Exiting.'.format(backup_user))
        # source
        source = config.get(self.SECTION, 'SOURCE', fallback=None)
        self.source = source.split(',') if source is not None else None
        # --backup-dir
        backup_dir = kwargs.get('backup_dir') or config.get(
            self.SECTION, 'BACKUP_DIR', fallback=None)
        if backup_dir is None or len(backup_dir) == 0:
            raise Exception('BACKUP_DIR is not configured')
        if not os.path.isabs(backup_dir):
            base_dir = config.get('DEFAULT', 'BACKUP_DIR', fallback=None)
            if base_dir is not None:
                backup_dir = os.path.join(base_dir, backup_dir)
        self.backup_dir = os.path.abspath(backup_dir)
        # --rotate
        self.rotate = kwargs.get('rotate') or config.getint(
            self.SECTION, 'ROTATE', fallback=0)
        # --tmp-dir
        self.tmp_dir = kwargs.get('tmp_dir') or config.get(
            self.SECTION, 'TMP_DIR', fallback=tempfile.gettempdir())
        # Encryptor
        encryptor_name = kwargs.get('encryptor') or config.get(
                self.SECTION, 'ENCRYPTOR', fallback=None)
        self.encryptor = encrypt.make_encryptor(
            encryptor_name,
            config=config,
            section=self.SECTION,
            **kwargs,
        )
        # Archiver
        archiver_name = kwargs.get('archiver') or config.get(
            self.SECTION,
            'ARCHIVER',
            fallback='tar',
        )
        self.archiver = archive.make_archiver(
            name=archiver_name,
            config=config,
            section=self.SECTION,
            **kwargs,
        )
        # Archive file suffix
        suffix = self.archiver.suffix
        if self.encryptor is not None:
            suffix += self.encryptor.suffix
        self.suffix = suffix
        self.progress_suffix = config.get(
            self.SECTION,
            'PROGRESS_SUFFIX',
            fallback='.in_progress',
        )
        # EXCLUDE
        exclude = kwargs.get('exclude', [])
        if len(exclude) == 0:
            exclude_conf = config.get(self.SECTION, 'EXCLUDE', fallback=None)
            if exclude_conf is not None:
                exclude.extend(utils.dequote(exclude_conf).split(','))
        self.exclude = exclude if len(exclude) > 0 else None
        # EXCLUDE_FROM
        exclude_from = kwargs.get('exclude_from', [])
        if len(exclude_from) == 0:
            exclude_from_conf = config.get(
                self.SECTION,
                'EXCLUDE_FROM',
                fallback=None,
            )
            if exclude_from_conf is not None:
                for exf in utils.dequote(exclude_from_conf).split(','):
                    exf = utils.dequote(exf)
                    if exf == '':
                        continue
                    exclude_from.append(exf)
        self.exclude_from = exclude_from if len(exclude_from) > 0 else None
        # compressor
        compressor_cmd = kwargs.get('compressor_cmd') or config.get(
            section=self.SECTION,
            option='COMPRESSOR_COMMAND',
            fallback='/bin/gzip -q9',
        )
        self.compressor_cmd = compressor_cmd.split(' ')
        self.compressor_suffix = config.get(
            section=self.SECTION,
            option='COMPRESSOR_SUFFIX',
            fallback='.gz',
        )
        # File methods.
        self.open = open

    def _relative_to_abs(self, file_path):
        """Преобразование относительного пути в абсолютный."""
        if os.path.isabs(file_path):
            return file_path
        if self.config_file_dir is None:
            return file_path
        return os.path.join(self.config_file_dir, file_path)

    def _load_exclude_file(self, filepath):
        """Загрузка файла с шаблонами исключения из архива в список строк."""
        exclude = []
        with self.open(self._relative_to_abs(filepath), 'r') as ex_file:
            for line in ex_file.readlines():
                exv = utils.dequote(line.strip())
                if exv != '':
                    exclude.append(exv)
        return exclude

    def _compress(self, in_stream, out_stream):
        """Сжатие потока in_stream в выходной поток out_stream."""
        subprocess.check_call(
            self.compressor_cmd,
            stdin=in_stream,
            stdout=out_stream,
            stderr=self.stream_err,
        )

    def outpath(self, name, **kwargs):
        """
        Формирование имени файла с архивом.

        :param name: Имя файла архива без расширения.
        :type name: str
        :return: Полный путь к файлу с архивом.
        :rtype: str
        """
        return os.path.join(self.backup_dir, name + self.suffix)

    def pack(self, *args, **kwargs):
        """Архивация файлов или папки."""
        self.archiver.pack(*args, **kwargs)

    def backup(self, sources=None, verbose=False, **kwargs):
        """
        Архивация источников в заданную папку с архивами.

        :param sources: Список источников архива.
        :type sources: [str]
        :param verbose: Выводить сообщения.
        :type verbose: bool
        :return: Код возврата.
        :rtype: int
        """
        if verbose:
            self.out('Backup started.\n', '----------------------')
        if sources is None or len(sources) == 0:
            sources = self.source
        if not os.path.exists(self.backup_dir):
            if verbose:
                self.out('Making backup directory in ', self.backup_dir)
            try:
                os.makedirs(self.backup_dir, mode=self.BACKUP_DIR_PERMISSIONS)
            except Exception as ex:
                self.err(
                    'Error creating backup directory "',
                    self.backup_dir, '": ', str(ex),
                )
                raise
        if verbose:
            self.out('\nPerforming backups\n', '----------------------')
        error_count = self._backup(
            sources=sources,
            verbose=verbose,
            **kwargs,
        )
        if verbose:
            self.out('----------------------\n', 'All backups complete!')
        if error_count != 0:
            self.err('Errors occurred, number of errors: ', str(error_count))
        return 0 if error_count == 0 else 1

    def archive(self, source, output, **kwargs):
        """
        Упаковка источника в файл с архивом.

        При необхододимости выполняется ротация архивных файлов с таким же
        именем (без числового расширения), что и результирующий архив.

        :param source: Источник или список источников для архивации.
        :type source: str или [str]
        :param output: Путь к файлу с архивом.
        :type output: str
        :param base_dir: Путь к базовой папке источников.
        :type base_dir: str
        """
        out = os.path.join(
            self.tmp_dir,
            os.path.basename(output) + self.progress_suffix,
        )
        self._archive(source=source, output=out, **kwargs)
        if self.rotate > 0:
            pos = len(output) + 1
            rlist = []
            for archive_file in glob.iglob(output + '.*'):
                ext = archive_file[pos:]
                if ext.isdigit():
                    rlist.append((int(ext), archive_file))
            rlist.sort(key=lambda item: item[0], reverse=True)
            if rlist:
                for item in rlist:
                    if item[0] > self.rotate:
                        os.remove(item[1])
            if os.path.isfile(output):
                for item in rlist:
                    num = item[0]
                    if num < self.rotate:
                        shutil.move(item[1], output + '.' + str(num + 1))
                os.rename(output, output + '.1')
        if self.encryptor is not None:
            try:
                self.encryptor.encrypt(source=out, output=output)
            except Exception:
                raise
            finally:
                os.remove(out)
        else:
            shutil.move(out, output)
        os.chmod(output, self.ARCHIVE_PERMISSIONS)

    @abc.abstractmethod
    def _backup(self, sources=None, verbose=False, **kwargs):
        """
        Архивация набора источников.

        :param source: Список источников для архивации.
        :type source: [str]
        :param verbose: Выводить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """

    @abc.abstractmethod
    def _archive(self, source, output, **kwargs):
        """
        Упаковка источника в файл с архивом.

        :param source: Источник или список источников для архивации.
        :type source: str или [str]
        :param output: Путь к файлу с архивом.
        :type output: str
        :param base_dir: Путь к базовой папке источников.
        :type base_dir: str
        """

    def out(self, *args, end='\n'):
        """Вывод информационного сообщения в поток."""
        for data in args:
            if isinstance(data, bytes):
                data = data.decode(self.encoding)
            self.stream_out.write(data)
        else:
            self.stream_out.write(end)

    def err(self, *args, end='\n'):
        """Вывод сообщения об исключительной ситуации в поток."""
        for data in args:
            if isinstance(data, bytes):
                data = data.decode(self.encoding)
            self.stream_err.write(data)
        else:
            self.stream_err.write(end)
