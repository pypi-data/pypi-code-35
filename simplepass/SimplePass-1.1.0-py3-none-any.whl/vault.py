import os
import base64
import pickle

from passlib.hash import pbkdf2_sha256 as p_hash
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def getkey(master):
    password = master.encode()
    salt = b'EC6873C47AD2F3FABCCC62AF564996F3F84ECD446433DDE'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def get_salt():
    return os.urandom(16)


def encrypt(key, salt, password):
    f = Fernet(key)
    encrypted = f.encrypt(password)
    return encrypted


def decrypt(key, salt, password):
    f = Fernet(key)
    decrypted = f.decrypt(password)
    return decrypted


def pickle_bytes(token):
    p = pickle.dumps(token)
    return base64.b64encode(p).decode('ascii')


def unpickle_string(token):
    p = base64.b64decode(token)
    return pickle.loads(p)


def lock(key, salt1, salt2, password):
    encrypted = pickle_bytes(
        encrypt(key, salt2, encrypt(key, salt1, password)))
    return encrypted


def unlock(key, salt1, salt2, token):
    decrypted = decrypt(
        key, salt1, decrypt(key, salt2,
                            unpickle_string(token)))
    return decrypted.decode()
