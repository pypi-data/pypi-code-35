# -*- coding: utf-8 -*-
"""Модуль шифровальщиков."""

import subprocess


class Gpg(object):
    """Шифровальщик посредством утилиты GnuPG."""

    SECTION = 'Encrypt-GnuPG'

    def __init__(self, config):
        """
        Конструктор.

        :param config: Конфигурация.
        :type config: :class:`ConfigParser.RawConfigParser`
        """
        self.cmd = config.get(self.SECTION, 'COMMAND', fallback='/usr/bin/gpg')
        self.recipient = config.get(self.SECTION, 'RECIPIENT', fallback=None)
        self.suffix = config.get(self.SECTION, 'SUFFIX', fallback='.gpg')

    def encrypt(self, source, output=None):
        """
        Шифрование файла.

        :param source: Путь к шифруемому файлу.
        :type source: str
        :param output: Путь к зашифрованному файлу.
        :type output: str
        :param compress_level: Уровень сжатия зашифрованного файла.
        :type compress_level: int
        """
        params = [self.cmd, '--quiet', '--batch']
        if output is None:
            output = source + self.suffix
        params.append('--output')
        params.append(output)
        if self.recipient is not None:
            params.append('--recipient')
            params.append(self.recipient)
        else:
            params.append('--default-recipient-self')
        params.append('--encrypt')
        params.append(source)
        subprocess.run(
            params,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=True,
        )


# Encryptors map.
ENCRYPTORS = {
    'gpg': Gpg,  # Use gnupg encryptor.
}


def make_encryptor(name, *args, **kwargs):
    """
    Фабрика шифровальщика.

    :param name: Имя шифровальщика.
    :type name: str
    :param config: Конфигурация.
    :type config: :class:`ConfigParser.RawConfigParser`
    """
    if name is None:
        return None
    if name not in ENCRYPTORS:
        raise Exception('Unknown encryptor: {}'.format(name))
    return ENCRYPTORS[name](*args, **kwargs)
