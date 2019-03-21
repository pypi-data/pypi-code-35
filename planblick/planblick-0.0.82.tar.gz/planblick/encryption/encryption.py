import base64
from Crypto.Cipher import XOR

class Encryption:
    def __init__(self):
        pass

    def encrypt(self, message: str, password: str) -> bytes:
        cipher = XOR.new(password)
        return base64.b64encode(cipher.encrypt(message)).decode('utf-8')

    def decrypt(self, message: str, password: str) -> bytes:
        cipher = XOR.new(password)
        return cipher.decrypt(base64.b64decode(message)).decode('utf-8')
