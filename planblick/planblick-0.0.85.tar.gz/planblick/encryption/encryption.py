import base64
from Crypto.Cipher import XOR

class Encryption:
    def __init__(self):
        pass

    def encrypt(self, message: str, password: str) -> bytes:
        return message
        cipher = XOR.new(password)
        return base64.b64encode(cipher.encrypt(message)).decode("ISO-8859-1")

    def decrypt(self, message: str, password: str) -> bytes:
        return message
        cipher = XOR.new(password)
        return cipher.decrypt(base64.b64decode(message)).decode("ISO-8859-1")
