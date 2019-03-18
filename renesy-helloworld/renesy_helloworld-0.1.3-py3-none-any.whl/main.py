import sys

from Crypto.Cipher import AES

def main(argv=None):
    if argv is None:
        argv = sys.argv

    obj = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
    message = "Hello, world"
    ciphertext = obj.encrypt(message)
    print(ciphertext)
    obj2 = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
    decipher_message = obj2.decrypt(ciphertext).decode()
    print(f">{decipher_message}<")

    return 0
