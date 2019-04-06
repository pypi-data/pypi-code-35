#!/usr/bin/env python
# -*- conding: utf-8 -*-


import os
import binascii
from .cryptile_parse import parse_args
from .cryptile import crypt_data


def main():
    """Main function to be called by the script cryptile."""

    args = parse_args()
    _crypt = crypt_data(args.key)

    if args.file and os.path.exists(args.file):
        _file = open(args.file, 'r').read()
        with open(args.file, 'w') as crypt_file:
            if args.encrypt:
                crypt_file.write(_crypt.encrypt(_file).decode())
            if args.decrypt:
                try:
                    crypt_file.write(_crypt.decrypt(_file).decode())
                except binascii.Error:
                    print("This do not contaim a base64 data.")

    if args.string:
        if args.encrypt:
            print(_crypt.encrypt(args.string).decode())
        try:
            if args.decrypt:
                print(_crypt.decrypt(args.string).decode())
        except binascii.Error:
                print("This string is not a base64 string.")

if __name__ == "__main__":
    main()