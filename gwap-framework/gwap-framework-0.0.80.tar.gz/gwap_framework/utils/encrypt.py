import codecs
from base64 import b64decode, b64encode
from typing import Union

from Crypto.Cipher import AES
from Crypto.Util import Counter
from cffi.backend_ctypes import long
from decouple import config
from sqlalchemy import TypeDecorator, String


def encrypt(value: str) -> Union[str, None]:
    """
    Encrypt a string using AES 256
    :param value: String
    :return: String or None
    """
    if value is None or not isinstance(value, str):
        return value

    iv = config('CRYPT_IV').encode()
    key = config('CRYPT_KEY').encode()[:32]
    ctr = Counter.new(
        128, initial_value=long(codecs.encode(iv, "hex_codec"), 16))

    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    encrypt_value = aes.encrypt(value.encode())
    return b64encode(encrypt_value).decode()


def decrypt(value: str) -> Union[str, None]:
    """
    Encrypt a string using AES 256
    :param value: String
    :return: String or None
    """
    if value is None or not isinstance(value, str):
        return value

    iv = config('CRYPT_IV').encode()
    key = config('CRYPT_KEY').encode()[:32]
    ctr = Counter.new(
        128, initial_value=long(codecs.encode(iv, "hex_codec"), 16))

    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    decrypted_value = aes.decrypt(b64decode(value))
    return decrypted_value.decode()


class EncryptedValue(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect) -> Union[str, None]:
        return encrypt(value)

    def process_result_value(self, value, dialect) -> Union[str, None]:
        return decrypt(value)
