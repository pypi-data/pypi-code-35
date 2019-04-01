import base64
import binascii
import os

from pkiexpress.utils import _base64_encode_string
from .auth_complete_result import AuthCompleteResult
from .auth_start_result import AuthStartResult
from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class Authentication(PkiExpressOperator):

    def __init__(self, config=None):
        if config is None:
            config = PkiExpressConfig()
        super(Authentication, self).__init__(config)

        self.__nonce = None
        self.__certificate_path = None
        self.__signature = None
        self.__use_external_storage = False

    # region "nonce" accessors

    @property
    def nonce(self):
        return self.__get_nonce()

    def __get_nonce(self):
        return self.__nonce

    @nonce.setter
    def nonce(self, value):
        self.__set_nonce(value)

    def __set_nonce(self, value):
        if value is None:
            raise Exception('The provided "nonce" is not valid')
        self.__nonce = value

    # endregion

    # region "nonce_base64" accessors

    @property
    def nonce_base64(self):
        return self.__get_nonce_base64()

    def __get_nonce_base64(self):
        nonce_raw = self.__get_nonce()
        if nonce_raw is None:
            return None
        return _base64_encode_string(nonce_raw)

    @nonce_base64.setter
    def nonce_base64(self, value):
        self.__set_nonce_base64(value)

    def __set_nonce_base64(self, value):
        if value is None:
            raise Exception('The provided "nonce_base64" is not valid')
        self.__nonce = base64.standard_b64decode(value)

    # endregion

    # region "certificate_path" accessors

    @property
    def certificate_path(self):
        return self.__get_certificate_path()

    def __get_certificate_path(self):
        return self.__certificate_path

    @certificate_path.setter
    def certificate_path(self, value):
        self.__set_certificate_path(value)

    def __set_certificate_path(self, value):
        if value is None:
            raise Exception('The provided "certificate_path" is not valid')
        if not os.path.exists(value):
            raise Exception('The provided certificate was not found')
        self.__certificate_path = value

    # endregion

    # region "certificate_raw" accessors

    @property
    def certificate_raw(self):
        return self.__get_certificate_raw()

    def __get_certificate_raw(self):
        if self.__certificate_path is None:
            return None
        with open(self.__certificate_path) as f:
            content_raw = f.read()
        return content_raw

    @certificate_raw.setter
    def certificate_raw(self, value):
        self.__set_certificate_raw(value)

    def __set_certificate_raw(self, value):
        if value is None:
            raise Exception('The provided "certificate_raw" is not valid')
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(value)
        self.__certificate_path = temp_file_path

    # endregion

    # region "certificate_base64" accessors

    @property
    def certificate_base64(self):
        return self.__get_certificate_base64()

    def __get_certificate_base64(self):
        content_raw = self.__get_certificate_raw()
        if content_raw is None:
            return None
        return _base64_encode_string(content_raw)

    @certificate_base64.setter
    def certificate_base64(self, value):
        self.__set_certificate_base64(value)

    def __set_certificate_base64(self, value):
        if value is None:
            raise Exception('The provided "certificate_base64" is not valid')
        try:
            raw = base64.standard_b64decode(str(value))
        except (TypeError, binascii.Error):
            raise Exception('The provided certificate is not Base64-encoded')
        self.__set_certificate_raw(raw)

    # endregion

    # region "signature" accessors

    @property
    def signature(self):
        return self.__get_signature()

    def __get_signature(self):
        return self.__signature

    @signature.setter
    def signature(self, value):
        self.__set_signature(value)

    def __set_signature(self, value):
        if value is None:
            raise Exception('The provided "signature" is not valid')
        self.__signature = value

    # endregion

    # region "signature_base64" accessors

    @property
    def signature_base64(self):
        return self.__get_signature_base64()

    def __get_signature_base64(self):
        signature_raw = self.__get_signature()
        if signature_raw is None:
            return None
        return _base64_encode_string(signature_raw)

    @signature_base64.setter
    def signature_base64(self, value):
        self.__set_signature_base64(value)

    def __set_signature_base64(self, value):
        if value is None:
            raise Exception('The provided "signature_base64" is not valid')
        try:
            raw = base64.standard_b64decode(str(value))
        except (TypeError, binascii.Error):
            raise Exception('The provided signature is not Base64-encoded')
        self.__set_signature(raw)

    # endregion

    # region "use_external_storage" accessors

    @property
    def use_external_storage(self):
        return self.__get_use_external_storage()

    def __get_use_external_storage(self):
        return self.__use_external_storage

    @use_external_storage.setter
    def use_external_storage(self, value):
        self.__set_use_external_storage(value)

    def __set_use_external_storage(self, value):
        if value is None:
            raise Exception('The provided "use_external_storage" is not valid')
        self.__use_external_storage = value

    # endregion

    def start(self):
        args = []

        # The option "use external storage" is used to ignore the PKI Express's
        # nonce verification, to make a own nonce store and nonce verification.
        if self.__use_external_storage:
            args.append('--nonce-store')
            args.append(str(self._config.transfer_data_folder))

        # This operation can only be used on versions greater then 1.4 of PKI
        # Express.
        self._version_manager.require_version('1.4')

        # Invoke command.
        response = self._invoke(self.COMMAND_START_AUTH, args)

        # Parse output and return result.
        model = self._parse_output(response[0])
        return AuthStartResult(model)

    def complete(self):
        if self.__nonce is None:
            raise Exception('The nonce was not set')

        if self.__certificate_path is None:
            raise Exception('The certificate file was not set')

        if self.__signature is None:
            raise Exception('The signature was not set')

        args = [
            self.__get_nonce_base64(),
            self.__certificate_path,
            self.__get_signature_base64()
        ]

        # The option "use external storage" is used to ignore the PKI Express's
        # nonce verification, to make a own nonce store and nonce verification.
        if self.__use_external_storage:
            args.append('--nonce-store')
            args.append(str(self._config.transfer_data_folder))

        # This operation can only be used on versions greater then 1.4 of PKI
        # Express.
        self._version_manager.require_version('1.4')

        # Invoke command.
        response = self._invoke(self.COMMAND_COMPLETE_AUTH, args)

        # Parse output and return result.
        model = self._parse_output(response[0])
        return AuthCompleteResult(model)


__all__ = ['Authentication']
