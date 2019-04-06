#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Crypto.Cipher import XOR
import base64


class crypt_data(object):

    def __init__(self, _key):
        """Init self.key like XOR object."""

        self.key = _key

    def encrypt(self, _text):
        """Return encrypted text."""

        cipher = XOR.new(self.key)
        return base64.b64encode(cipher.encrypt(_text))

    def decrypt(self, _text):
        """Return decrypted text."""

        cipher = XOR.new(self.key)
        return cipher.decrypt(base64.b64decode(_text))