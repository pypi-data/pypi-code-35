import os
import base64
from cryptography.fernet import Fernet
from cleo import Application, Command as BaseCommand
from typing import Optional


class Command(BaseCommand):
    @property
    def secret_key(self) -> Optional[str]:
        try:
            return os.environ['OLAS_SECURITYCONFIG_HASH'][:32]
        except KeyError:
            self.line('<error>Unable to perform encrypt/decrypt operations because the environmental variable '
                      '`OLAS_SECURITYCONFIG_HASH` is not set</error>')
            return None


class EncryptCommand(Command):
    """
    Encrypts a given value

    encrypt
        {value : The value to encrypt}
        {--k|key : The key to encrypt against}

    """

    def handle(self) -> None:
        value = self.argument('value')
        key = self.option('key')

        if key:
            SECRET_KEY = key
        else:
            SECRET_KEY = self.secret_key

        if SECRET_KEY:
            key = base64.urlsafe_b64encode(bytes(SECRET_KEY.encode()))
            cipher_suite = Fernet(key)
            plain_text = cipher_suite.encrypt(value.encode())
            self.line('<info>ENCRYPTED VALUE:</info>')
            self.line(f'<info>{plain_text.decode()}</info>')


class DecryptCommand(Command):
    """
    Decrypts a given value

    decrypt
        {value : The value to decrypt}
        {--k|key : The key decrypt against}
    """

    def handle(self) -> None:
        cipher_text = self.argument('cipher-text')
        key = self.option('key')

        if key:
            SECRET_KEY = key
        else:
            SECRET_KEY = self.secret_key

        if SECRET_KEY:
            key = base64.urlsafe_b64encode(bytes(SECRET_KEY.encode()))
            cipher_suite = Fernet(key)
            plain_text = cipher_suite.decrypt(cipher_text.encode())
            self.line('<info>DECRYPTED VALUE:</info>')
            self.line(f'<info>{plain_text.decode()}</info>')


application = Application()
application.add(DecryptCommand())
application.add(EncryptCommand())
application.run()
