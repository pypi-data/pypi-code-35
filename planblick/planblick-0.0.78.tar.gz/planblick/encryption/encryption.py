import secrets
import base64
from Crypto.Cipher import XOR

class Encryption:
    def __init__(self):

    def encrypt(self, message: str, password: str) -> bytes:
        cipher = XOR.new(password)
        return base64.b64encode(cipher.encrypt(message))

    def decrypt(self, message: str, password: str) -> bytes:
        cipher = XOR.new(password)
        return cipher.decrypt(base64.b64decode(message))
