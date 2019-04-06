#!/usr/bin/env python
# -*- coding: utf-8 -*-


from argparse import ArgumentParser


def parse_args():
    """Define some args for cryptile."""

    _parser = ArgumentParser(add_help=True, description=("""
  Cryptile returns a string or file encrypted with a key.

  USAGE: cryptile [-f|-s] [string|path] -k passkey.
  Cryptile encrypt a file or string by time, do not use -f and -s together.
  """))

    _parser.add_argument('-f', '--file', action='store', required=False,
                         help="Get the file path to encrypt.")
    _parser.add_argument('-s', '--string', action='store', required=False,
                         help="Get the string to encrypt.")
    _parser.add_argument('-k', '--key', action='store', required=True,
                         help="Get a string key to encrypt data.")
    _parser.add_argument('-e', '--encrypt', action='store_true', required=False,
                         help="Encrypt data.")
    _parser.add_argument('-d', '--decrypt', action='store_true', required=False,
                         help="Decrypt data.")

    return _parser.parse_args()