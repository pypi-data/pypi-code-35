from base64 import b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers

from .exceptions import RequestException
from .utils import retry


class Authenticator:
    def __init__(self, request_executor, login, password):
        self.request_executor = request_executor
        self.login = login
        self.password = password
        self._encrypted_password = None
        self._token = None

    @retry((RequestException,))
    def _get_token(self):
        data = {
            'operation': 'get_token',
            'login': self.login,
        }
        json_data = self.request_executor.request(data=data)
        return json_data

    def setup(self):
        token_response = self._get_token()
        self._token = token_response['data']['token']
        self._encrypted_password = EncryptedPassword(
            self.password, token_response['data']['modulus'], token_response['data']['exponent'])

    @property
    def encrypted_password(self):
        if self._encrypted_password is None:
            self.setup()
        return self._encrypted_password

    @property
    def token(self):
        if self._token is None:
            self.setup()
        return self._token


class EncryptedPassword:
    """
    PKCS1 v1.5 encrypted password.
    """

    def __init__(self, password, modulus, exponent):
        self._password = password.encode('utf-8')
        modulus = int(modulus, 16)
        exponent = int(exponent, 16)
        public_numbers = RSAPublicNumbers(exponent, modulus)
        self.public_key = public_numbers.public_key(default_backend())

    @property
    def password(self):
        return self.public_key.encrypt(self._password, padding.PKCS1v15()).hex()


class Signer:
    def __init__(self, private_key: bytes):
        self._key = serialization.load_pem_private_key(private_key, None, default_backend())

    def sign(self, message):
        signature = self._key.sign(message, padding.PKCS1v15(), hashes.SHA1())
        signature = b64encode(signature)
        return signature
