# -*- coding: utf-8 -*-
"""Модуль архиватора баз данных PostgreSQL."""

import os
import sys
import subprocess

from msbackup import backend_base, utils


class PostgreSQL(backend_base.Base):
    """Архиватор баз данных PostgreSQL."""

    SECTION = 'Backend-PostgreSQL'

    FORMAT_NONE = 0  # Формат архива не задан.
    FORMAT_PLAIN = 1  # Полный архив БД в текстовом формате.
    FORMAT_CUSTOM = 2  # Полный архив БД в сжатом формате.

    FORMAT_MAP = {
        'plain': FORMAT_PLAIN,
        'custom': FORMAT_CUSTOM,
        'default': FORMAT_NONE,
    }
    MODE_NONE = 0  # Запрет архивирования БД.
    MODE_SCHEMA = 1  # Архивировать только схему БД.
    MODE_FULL = 2  # Полный архив БД.

    def __init__(self, config, **kwargs):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        :param out: Поток вывода информационных сообщений.
        :param err: Поток вывода сообщений об ошибках.
        :param encryptor: Имя шифровальщика.
        :type encryptor: str
        """
        super().__init__(config, **kwargs)
        # config file options
        self.host = kwargs.get('host') or config.get(
            section=self.SECTION, option='HOST', fallback=None)
        self.port = kwargs.get('port') or config.get(
            section=self.SECTION, option='PORT', fallback=None)
        self.username = kwargs.get('username') or config.get(
            section=self.SECTION,
            option='USERNAME',
            fallback=None,
        )
        format_name = config.get(
            section=self.SECTION, option='BACKUP_FORMAT', fallback='plain')
        if format_name in self.FORMAT_MAP:
            self.format = self.FORMAT_MAP[format_name]
        else:
            raise Exception('Invalid backup format name: {}'
                            .format(format_name))
        # schema_only_list
        self.schema_only_list = []
        lst = utils.dequote(config.get(
            section=self.SECTION,
            option='SCHEMA_ONLY_LIST',
            fallback='',
        ))
        if lst:
            self.schema_only_list.extend(lst.split(' '))
        # psql_cmd
        self.psql_cmd = config.get(
            section=self.SECTION,
            option='PSQL_COMMAND',
            fallback='/usr/bin/psql',
        )
        # pgdump_cmd
        self.pgdump_cmd = config.get(
            section=self.SECTION,
            option='PGDUMP_COMMAND',
            fallback='/usr/bin/pg_dump',
        )
        # compressor
        self.compressor_cmd = [config.get(
            section=self.SECTION,
            option='COMPRESSOR_COMMAND',
            fallback='/bin/gzip',
        )]
        compressor_params = config.get(
            section=self.SECTION,
            option='COMPRESSOR_PARAMS',
            fallback='-q9',
        ).split(' ')
        self.compressor_cmd.extend(compressor_params)
        self.compressor_suffix = config.get(
            section=self.SECTION,
            option='COMPRESSOR_SUFFIX',
            fallback='.gz',
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

        :param name: Имя файла архива без расширения.
        :type name: str
        :param mode: Режим архивации базы данных.
        :type mode: int
        :return: Полный путь к файлу с архивом.
        :rtype: str
        """
        fname = name
        if kwargs.get('mode', self.MODE_NONE) == self.MODE_SCHEMA:
            fname += '_SCHEMA.sql'
            fname += self.compressor_suffix
        elif self.format == self.FORMAT_PLAIN:
            fname += '.sql'
            fname += self.compressor_suffix
        elif self.format == self.FORMAT_CUSTOM:
            fname += '.custom'
        else:
            fname += self.compressor_suffix
        if self.encryptor is not None:
            fname += self.encryptor.suffix
        return os.path.join(self.backup_dir, fname)

    def _archive(self, source, output, **kwargs):
        """
        Архивация одной базы данных PostgreSQL.

        :param source: Имя базы данных.
        :type source: str
        :param output: Путь к файлу с архивом.
        :type output: str
        """
        mode = kwargs.pop('mode', self.MODE_NONE)
        if self.format == self.FORMAT_CUSTOM:
            subprocess.check_call(self._dump_params(
                database=source,
                output=output,
                mode=mode,
                **kwargs,
            ))
        else:
            p1 = self._dump_proc(
                database=source,
                output=output,
                mode=mode,
                stdout=subprocess.PIPE,
                **kwargs,
            )
            with self.open(output, 'wb') as out:
                self._compress(in_stream=p1.stdout, out_stream=out)

    def _backup(self, sources=None, verbose=False, **kwargs):
        """
        Архивация баз данных PostgreSQL на заданном узле.

        :param sources: Список имён баз данных для архивации.
        :type sources: [str]
        :param base_dir: Путь к папке с источниками (игнорируется).
        :type base_dir: str
        :param verbose: Выводить информационные сообщения.
        :type verbose: bool
        :return: Количество ошибок.
        :rtype: int
        """
        dblist = sources if sources is not None else self.dblist(**kwargs)
        error_count = 0
        for database in dblist:
            if self.exclude is not None and database in self.exclude:
                continue
            mode = (self.MODE_SCHEMA if database in self.schema_only_list
                    else self.MODE_FULL)
            if verbose is True:
                info = ''
                if mode == self.MODE_SCHEMA:
                    info = 'Schema-only'
                elif self.format == self.FORMAT_PLAIN:
                    info = 'Plain'
                elif self.format == self.FORMAT_CUSTOM:
                    info = 'Custom'
                else:
                    info = 'Default'
                self.out(info, ' backup database: ', database)
            try:
                self.archive(
                    source=database,
                    output=self.outpath(name=database, mode=mode),
                    mode=mode,
                    **kwargs,
                )
            except subprocess.CalledProcessError as ex:
                error_count += 1
                self.err(ex.stderr)
        return error_count

    def dblist(self, **kwargs):
        """
        Список имён баз данных.

        :return: Список имён всех баз данных.
        :rtype: [str]
        """
        params = [self.psql_cmd]
        if self.host or 'host' in kwargs:
            params.append('--host={}'.format(
                kwargs.get('host', self.host)))
        if self.port or 'port' in kwargs:
            params.append('--port={}'.format(
                kwargs.get('port', self.port)))
        if self.username or 'username' in kwargs:
            params.append('--username={}'.format(
                kwargs.get('username', self.username)))
        params.append('--no-password')
        params.append('--no-align')
        params.append('--tuples-only')
        params.append('-c')
        params.append('SELECT datname '
                      'FROM pg_database '
                      'WHERE NOT datistemplate '
                      'ORDER BY datname;')
        params.append('postgres')
        out = subprocess.check_output(params)
        return out.decode(sys.getdefaultencoding()).splitlines()

    def _dump_params(self, database, output, mode, stdout=None, **kwargs):
        """
        Подготовка процесса создания архива базы данных PostgreSQL.

        :param database: Имя базы данных.
        :type database: str
        :param output: Путь к файлу с архивом.
        :type output: str
        :param mode: Режим архивации базы данных.
        :type mode: int
        :param stdout: Поток вывода для процесса создания архива..
        """
        params = [self.pgdump_cmd]
        if mode == self.MODE_SCHEMA or self.format == self.FORMAT_PLAIN:
            params.append('--format=p')
        elif self.format == self.FORMAT_CUSTOM:
            params.append('--format=c')
        if mode == self.MODE_SCHEMA:
            params.append('--schema-only')
        if self.host or 'host' in kwargs:
            params.append('--host={}'.format(
                kwargs.get('host', self.host)))
        if self.port or 'port' in kwargs:
            params.append('--port={}'.format(
                kwargs.get('port', self.port)))
        if self.username or 'username' in kwargs:
            params.append('--username={}'.format(
                kwargs.get('username', self.username)))
        params.append('--no-password')
        params.append('--oids')
        if self.format == self.FORMAT_CUSTOM:
            params.append('--file={}'.format(output))
        params.append(database)
        return params

    def _dump_proc(self, *args, **kwargs):
        """
        Подготовка процесса создания архива базы данных PostgreSQL.

        :param database: Имя базы данных.
        :type database: str
        :param output: Путь к файлу с архивом.
        :type output: str
        :param mode: Режим архивации базы данных.
        :type mode: int
        :param stdout: Поток вывода для процесса создания архива..
        """
        popen_kwargs = {}
        if 'stdout' in kwargs:
            popen_kwargs['stdout'] = kwargs['stdout']
        return subprocess.Popen(
            self._dump_params(*args, **kwargs),
            **popen_kwargs,
        )
