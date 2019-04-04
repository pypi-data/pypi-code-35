#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
# Author: yuyongpeng@hotmail.com
# Description:
#  

"""

from Crypto.PublicKey import RSA


# def encrypt(message):
#     externKey = "/Users/yuyongpeng/git/hard-chain/cport/oracle/contracts/myPublicKey.pem"
#     privatekey = open(externKey, "r")
#     encryptor = RSA.importKey(privatekey, passphrase="f00bar")
#     encriptedData = encryptor.encrypt(message, 0)
#     file = open("/Users/yuyongpeng/git/hard-chain/cport/oracle/contracts/cryptThingy.txt", "wb")
#     file.write(encriptedData[0])
#     file.close()
#
# def decrypt():
#     externKey="/Users/yuyongpeng/git/hard-chain/cport/oracle/contracts//myPrivateKey.pem"
#     publickey = open(externKey, "r")
#     decryptor = RSA.importKey(publickey, passphrase="f00bar")
#     retval=None
#     file = open("/Users/yuyongpeng/git/hard-chain/cport/oracle/contracts//cryptThingy.txt", "rb")
#     retval = decryptor.decrypt(file.read())
#     file.close()
#     return retval

# if __name__ == "__main__":
#     decryptedThingy=decrypt()
#     print "Decrypted: %s" % decryptedThingy


def test():
    import base64

    from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
    from Crypto.PublicKey import RSA

    message = b"this is test"

    rsa_private_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAz4C8rDjl6NAAvdUxLl7p8eA+xxc4Sa20puq2gFPk+8B5W30o+8xAaktLoji9wEsf7WTEllxZcIXw7d4K9b1M34ZDQT1iR4ZreB3GkxEXDeQIV3f/W7C3NL1bF5ePn7DRGZYKTEry8pp/lK/1ESP9Z+giaN29xm+jsmvNAOJlLjndn8nYcmA1sdDzuX8JSlZOiijAwyKUkwrBd+FqlhbAfF9ebcEgQcRISZsBMpcsZ66HQ0nvEnhmLzkfXxLUu2w7ccwLc/W7a4V1SNFEMZifRyiI7IhYYpRFw7egQN2RgzVWW/O6HKzk2Mxaz/6Y+HEehuDfRDn5MjMCkhnfbpRKKwIDAQABAoIBAD7xpkn32IYO0qrDCPAwCnc8ts5d1M1EzA/2EvZKfKOBd06xYMVA6ClWPdMvsx+pqj2w25Fg4iCoALWnLVvt2GvVpoEbxbw8ok0Fez8RaBTmn0EpPWTq7igpaIB3kTG3yTYhtW3/LkM5aooH9icE69GhMQ7udKrFIrr0yHMEOf0TNKBUNlwwHWJrpUuodXxIbERonkNdri1AnsWsnh4ePkKFlgaIdOZ24W4kHjfQAQkz3bPTjRzU5Q0LpkCpuYxk+TeOvR5tNPHXtzTWYek7JbCbnIKr1SiJx+ncwWM7QEnuvbzCU2VeTwb6Rq94WIg3RpfqSKJPr5w5e/df4jmi58ECgYEA74ty4UiChdp27/xvy2sJMilgkcL5Z0A+McPrjM82CqfPvr1+ZMBkTwuQGxFWlNtdE7DLpneVCWmzAexUJ02dFndSJMqsN81335VYfLc94qk5HXwmc9UBK7+qL2Ugyz76KoRGogqkKYw0ZR2kdpcNoXjQfeVgqrumt+jnZChpAl8CgYEA3cHPuDbdqqhcslz4+Zz8B0zWKN8Kj5CgG9ReEmJGpE6w5D7bds5iPcmp5xwFctuumAtroA/+bpGX/2oXc1nXucf/dI3AWoaBQrZ9iL6xfe7+ZPiRYuZjz3ygZ+Vcgp6xixbTT86jaIHwsD1wYtzOiiYOUBt4jDk89xookjpBg7UCgYEAtCriQOdUpHBoPKBVRV5AEGZmp7tJ8oqzPKLrK4E+WE1XR1MnGYhK6dj8jh9AS72iCAlVYuNWSToi1TN3KAiMOjWMpvd5CI+VtaiSYVtBRJWay75w/XYb51fFHNinDbdUWV4b8gym5Ej7r4HYDQoXyncf+VDooAF7p5+ZSg/Ky2kCgYAlVsv+Dab3ZE/vbH4zsX4yUHrC+QNTNxvuc6y/VbLlWaapV/gmIgwisUEde/di5qCYU1v04JyLy5IXXKrELn2Hd6iI3JFl7L35GLc8fjdup/5HzB7W00o9FpP/ynvwNn5YmChOiNG0+CQp2L6CtwFD+7JvRKDgo4ajaNEqBgsf/QKBgE6kbfW6FSpFdOs+2qpIXTEWnTqUC3WD1h1qB8G8J3Tn/o/bSm8C5lHmjmg9vRJtHisaoLyc2ikH7UZwPGU32340s22igkDZml730CKrYtnnBZAG+tIiERtI4Zj432X7qzBYgTgwO7wRAvds+WDCwwV5FMGNCzbPEXos8HmS0812\n-----END RSA PRIVATE KEY-----\n'

    rsa_public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz4C8rDjl6NAAvdUxLl7p8eA+xxc4Sa20puq2gFPk+8B5W30o+8xAaktLoji9wEsf7WTEllxZcIXw7d4K9b1M34ZDQT1iR4ZreB3GkxEXDeQIV3f/W7C3NL1bF5ePn7DRGZYKTEry8pp/lK/1ESP9Z+giaN29xm+jsmvNAOJlLjndn8nYcmA1sdDzuX8JSlZOiijAwyKUkwrBd+FqlhbAfF9ebcEgQcRISZsBMpcsZ66HQ0nvEnhmLzkfXxLUu2w7ccwLc/W7a4V1SNFEMZifRyiI7IhYYpRFw7egQN2RgzVWW/O6HKzk2Mxaz/6Y+HEehuDfRDn5MjMCkhnfbpRKKwIDAQAB\n-----END PUBLIC KEY-----\n'

    s = b'Ho8r8K07ZuhY8DAG5ACmCRx+8LPe7YJiZ3ZefgnCohjXlTaBxbIs5KbU5jdVvQF3qesImTRTULa7rka5Ms7ymey6OGceKc3wT1h6xp542qVzlhBK87bHE++IIJls73uVWii99c6x+ow2L5rrZtsgOZFn4CGDsDtlXK71zsvZfZxWWiQYy67G0AayzY2c621cZ55VWY6Z4CVgd5i6W1tnsLows3c8gMKBsozFLovGle5lp+sqL39fNdpwbEas3qfNbqxP0ujBOGM2JSajGlQcLrJPlPnQGoT3DIydgHXbmAvq3DkW5siQJWiA+UwG57cGSkUDneY+oowUGgYtPJrl0g=='
    rsakey = RSA.importKey(rsa_public_key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(message))
    print(cipher_text)

    from oracle.crypto import encrypt2, decrypt2

    p = encrypt2(message, rsa_public_key)
    print(p)
    print(decrypt2(s, rsa_private_key))

    # rsakey = RSA.importKey(rsa_private_key)
    # cipher = Cipher_pkcs1_v1_5.new(rsakey)
    # text = cipher.decrypt(base64.b64decode(cipher_text), None)
    # print(text.decode('utf8'))


import rsa
from rsa import PublicKey


# from oracle.crypoor import encrypt,decrypt


def test_cryptography():
    from oracle.crypto import generate_private_key, generate_public_key, decrypt_rsa, encrypt_rsa
    (private_key_obj, private_key_str) = generate_private_key()
    (public_key_obj, public_key_str) = generate_public_key(private_key_obj)
    print(private_key_str)
    print(public_key_str)
    message = "hello world"
    sec = encrypt_rsa(message, public_key_obj)
    print(sec)
    import base64
    print(base64.b64decode(sec))
    txt = decrypt_rsa(sec, private_key_obj)
    print(txt)
    # print(repr(base64.b64encode(sec)))


def test_ecies():
    from oracle.crypto import encrypt_ecies, check_ecies
    private_Key = '0x6a6d5f34772ef3ba498c5256aa8470d2401e82a5921cbef58ec0c52e4336b925'
    public_Key = '0x044af3c4d907a75e9349f362b0f854c7d74a89dad457df4f9cbf3c4f9e2f7fbcf8916ac219bb70e64777930b1e85d0a550e1e61ca94fa902dee419849a9a0efe8a'
    original_text = 'abcedf'
    iv = '0x0c174c174e0c5a1643177d2e4ed3de8a'
    ciphertext = '0xb7db50ee715d37c0b73c1f0dd022990a'
    ephemPublicKey = '0x04be7916ed4da0f8b5bf44a211b4a41ce0998664eb5350bf16337c61160706a1da7892fef570651084f95fcc4d8ff2133f854a7247af2235b90c20a805ca4cb35a'
    iv = '0x0c174c174e0c5a1643177d2e4ed3de8a'
    mac = '0x78c35d9d22fb1050458c7e41e788006a91b7ef59ddd985c013fc08049b8935ce'
    print(encrypt_ecies(public_Key, original_text, iv))
    # tx = check_ecies(private_key=private_key, ephemPublicKey=ephemPublicKey, ciphertext=ciphertext,verified_text='abcdef')
    # print(tx)


def test_iv():
    from oracle.crypto import get_iv
    import datetime
    now = datetime.datetime.now()
    get_iv('1357723206')


if __name__ == "__main__":
    # test_cryptography()
    # test_ecies()
    test_iv()

