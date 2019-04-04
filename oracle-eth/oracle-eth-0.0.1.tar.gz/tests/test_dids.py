#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
# Author: yuyongpeng@hotmail.com
# Description:
#  

"""
from oracle.dids import Did
import json


def test():
    did_json_str = """{"@context":"https://w3id.org/did/v1","id":"did:ethr:b2be7c8722935db16921d64ad0ddb5d47a52482a#soldier","publicKey":[{"id":"did:ethr:b2be7c8722935db16921d64ad0ddb5d47a52482a##proof","type":"EciesVerificationKey","controller":"did:ethr:b2be7c8722935db16921d64ad0ddb5d47a52482a","publicKeyHex":"0x04521fbe1f862845cb09ca6c0cdff00417d4a3bf3c04748806eb49079f5d2d5d555c6461ecc3760bd10de1bc7c77421f02bbe3642d6d3e35ee219f84a026478297"}],"authentication":[{"id":"did:ethr:decd6626f23bc43cb4d738cb0f2dde922d691fd2#proof","type":"EciesVerificationKey","controller":"did:ethr:decd6626f23bc43cb4d738cb0f2dde922d691fd2","publicKeyHex":"0x024af3c4d907a75e9349f362b0f854c7d74a89dad457df4f9cbf3c4f9e2f7fbcf8"}],"proof":"00a991c5346ffd5763c851610ef95254f2ec37a0b5d88f8f55d778411b29b1062db7485674c69003720077d07701a37c","created":1554035188114}"""
    sign_text = """f4e085e52a799d062ad35e66c5ce3c842bab6bf5168e1860c187b46d23b6c8053e1df712bcb2e4c4a5901c93c3c17842835092a503dd4e8c39a4c344bd4832b701"""
    # did_json_obj = json.loads(did_json_str)
    tf = Did.verify_did(did_json_str, sign_text)
    print(tf)
    private_key = '0x6a6d5f34772ef3ba498c5256aa8470d2401e82a5921cbef58ec0c52e4336b925'
    sign_msg = Did.sign_did(did_json_str, sign_text, private_key)
    print(sign_msg)


def test_decrypt():
    """ 测试加密解密 """
    str = '0x00a991c5346ffd5763c851610ef95254f2ec37a0b5d88f8f55d778411b29b1062db7485674c69003720077d07701a37c'
    publicKeyHex = '0x04521fbe1f862845cb09ca6c0cdff00417d4a3bf3c04748806eb49079f5d2d5d555c6461ecc3760bd10de1bc7c77421f02bbe3642d6d3e35ee219f84a026478297'
    privateKey = '0x6a6d5f34772ef3ba498c5256aa8470d2401e82a5921cbef58ec0c52e4336b925'
    from oracle.crypto import decrypt_ecies
    tf = decrypt_ecies(private_key=privateKey, ephemPublicKey=publicKeyHex, ciphertext=str)
    print(tf.lstrip(b'0x').decode())
    print(bytes.fromhex(tf.lstrip(b'0x')).decode())
    print(tf)


# 指定参数和返回类型
def say_hi(name: str = 'yyp') -> str:
    return "Hi," + name


if __name__ == '__main__':
    test()
    # from oracle.database.dbs import query_keys, db, query_contract
    # test_decrypt()






