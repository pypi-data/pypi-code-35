#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
# Author: yuyongpeng@hotmail.com
# Description: 用于签名和验证签名
#  

"""

from eth_keys import keys
from eth_utils import decode_hex, add_0x_prefix, to_hex, keccak, is_bytes
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend
import os
import re


def get_key_and_address(length=32):
    """
    生成16进制的private_key
    :param length:
    :return:
    """
    iv = os.urandom(length)
    private_key = to_hex(iv)
    public_Key = privatekey_to_publickey(private_key)
    address = privatekey_to_address(private_key)
    return private_key, address, public_Key


def privatekey_to_publickey(private_key):
    """
    生成私钥对应的公钥address
    :param private_key: 私钥 (hex或bytes）
    :return:
    """
    if not is_bytes(private_key):
        private_key = decode_hex(add_0x_prefix(private_key))
    pk = keys.PrivateKey(private_key)
    return pk.public_key


def privatekey_to_address(private_key):
    """
    根据私钥获得对应的公钥
    :param private_key: 私钥 （hex或bytes）
    :return:
    """
    if not is_bytes(private_key):
        private_key = decode_hex(add_0x_prefix(private_key))
    pk = keys.PrivateKey(private_key)
    return pk.public_key.to_checksum_address()


def sig_message(message, private_key_hex):
    """
    对message数据进行签名
    :param message: 需要签名的数据，(bytes)
    :param private_key_hex: 签名用的私钥
    :return:
    """
    private_key_byte = decode_hex(add_0x_prefix(private_key_hex))
    pk = keys.PrivateKey(private_key_byte)
    print('public key: {}'.format(pk.public_key))
    print('public key to address:  {}'.format(pk.public_key.to_checksum_address()))
    signature = pk.sign_msg(message)
    return signature


def ecdsa_sign(message: str, private_key_hex) -> str:
    """
    对message数据进行签名 (sig_message方法返回的结果相同)
    :param message: 需要签名的数据，(bytes)如果输入的不是byte会自动转成bytes
    :param private_key_hex: 签名用的私钥  str
    :return: str类型的签名数据 hex
    """
    if isinstance(message, str):
        message = message.encode('utf8')
    message_hash = keccak(message)
    keys_api = KeyAPI(NativeECCBackend())
    private_key_byte = decode_hex(add_0x_prefix(private_key_hex))
    pk = keys.PrivateKey(private_key_byte)
    signature = keys_api.ecdsa_sign(message_hash, pk)
    return str(signature).lstrip('0x')


def ecdsa_verify(message: str, signature: str, public_key):
    """
    验证签名是否正确
    :param message: 需要验证的数据 string
    :param signature: 签名 hex
    :param public_key: 必须是长的字符串，里面可能有前缀，需要处理  string or bytes
    :return:
    """
    if not isinstance(message, str):
        raise ValueError('message = {}  must string'.format(message))
    if not isinstance(signature, str):
        raise ValueError('signature = {}  must string'.format(signature))

    pb = check_public_key(public_key)   # pb 必须是一个没有 0x 和 04 前缀的 bytes
    message_hash = keccak(message.encode('utf8'))
    keys_api = KeyAPI(NativeECCBackend())
    signature_bytes = decode_hex(add_0x_prefix(signature))
    signature_obj = keys_api.Signature(signature_bytes=bytes.fromhex(signature))
    PublicKey = keys_api.ecdsa_recover(message_hash, signature_obj)
    # address_public = PublicKey.to_checksum_address()
    if '0x{}'.format(pb.decode()) == str(PublicKey):
        return True
    else:
        return False


def get_vrs_signature(signature_hex):
    """
    获得签名数据的 V R S
    :param signature_hex: 签名的数据 hex
    :return: (V, R, S)
    """
    keys_api = KeyAPI(NativeECCBackend())
    signature_bytes = decode_hex(signature_hex)
    signature_obj = keys_api.Signature(signature_bytes=signature_bytes)
    # return signature_obj.v, signature_obj.r, signature_obj.s
    return signature_obj.vrs


def value_to_hex(bts):
    """
    将二进制转换为hex（16进制）
    :param bts:
    :return:
    """
    return to_hex(bts)


def check_public_key(public_key):
    """
    监测public_key 返回正确的数据
    请注意，某些库在字节序列化公钥前面加上前导\x04字节，在使用PublicKey对象之前必须将其删除 。
    有一些public key 是带有前缀的，以太坊的public key 需要去掉前缀
    :param public_key: 公钥 (str 或者 bytes)
    :return:  返回bytes的字符串
    """
    if isinstance(public_key, bytes):
        public_key = public_key.decode()

    if isinstance(public_key, str):
        public_key_no0x = re.sub('^0x','',public_key)
        if len(public_key_no0x) == 128:
            public_key_str = public_key_no0x
        elif len(public_key_no0x) == 130:
            public_key_str = public_key_no0x[2:]
        else:
            raise ValueError('string public_key={} length not 128'.format(public_key))

    return public_key_str.encode()


def kaccke(value):
    """
    获得value对应的keccak的hash值
    :param value:
    :return: bytes数据
    """
    from eth_utils import keccak
    return keccak(value)
