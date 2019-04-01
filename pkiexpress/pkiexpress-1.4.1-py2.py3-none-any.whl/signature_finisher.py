import base64
import binascii
import json
import os

from .pk_certificate import PKCertificate
from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class SignatureFinisher(PkiExpressOperator):

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(SignatureFinisher, self).__init__(config)
        self.__file_to_sign_path = None
        self.__transfer_file_path = None
        self.__data_file_path = None
        self.__output_file_path = None
        self.__signature = None

    # region set_file_to_sign

    def set_file_to_sign_from_path(self, path):
        if not os.path.exists(path):
            raise Exception('The provided file to be signed was not found')
        self.__file_to_sign_path = path

    def set_file_to_sign_from_raw(self, content_raw):
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__file_to_sign_path = temp_file_path

    def set_file_to_sign_from_base64(self, content_base64):
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided file to be signed is not '
                            'Base64-encoded')
        self.set_file_to_sign_from_raw(raw)

    # endregion

    # region set_transfer_file

    def set_transfer_file_from_path(self, path):
        if not os.path.exists(os.path.join(self._config.transfer_data_folder,
                                           path)):
            raise Exception('The provided transfer file was not found')
        self.__transfer_file_path = path

    def set_transfer_file_from_raw(self, content_raw):
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__transfer_file_path = temp_file_path

    def set_transfer_file_from_base64(self, content_base64):
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided transfer file is not Base64-encoded')
        self.set_transfer_file_from_raw(raw)

    # endregion

    # region set_data_file

    def set_data_file_from_path(self, path):
        if not os.path.exists(path):
            raise Exception('The provided data file was not found')
        self.__data_file_path = path

    def set_data_file_from_raw(self, content_raw):
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__data_file_path = temp_file_path

    def set_data_file_from_base64(self, content_base64):
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided data file is not Base64-encoded')
        self.set_data_file_from_raw(raw)

    # endregion

    @property
    def signature(self):
        return self.__signature

    @signature.setter
    def signature(self, signature_base64):
        try:
            base64.standard_b64decode(str(signature_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided signature was not valid')
        self.__signature = signature_base64

    @property
    def output_file(self):
        return self.__output_file_path

    @output_file.setter
    def output_file(self, value):
        self.__output_file_path = value

    def complete(self, get_cert=False):
        if not self.__file_to_sign_path:
            raise Exception('The file to be signed was not set')

        if not self.__transfer_file_path:
            raise Exception('The transfer file was not set')

        if not self.__signature:
            raise Exception('The signature was not set')

        if not self.__output_file_path:
            raise Exception('The output destination was not set')

        args = [
            self.__file_to_sign_path,
            os.path.join(self._config.transfer_data_folder,
                         self.__transfer_file_path),
            self.__signature,
            self.__output_file_path
        ]

        if self.__data_file_path:
            args.append('--data-file')
            args.append(self.__data_file_path)

        if get_cert:
            # This operation can only be used on version greater than 1.8 of the
            # PKI Express
            self._version_manager.require_version('1.8')

            # Invoke command.
            result = self._invoke(self.COMMAND_COMPLETE_SIG, args)

            # Parse output and return model.
            model = json.loads(base64.standard_b64decode(result[0]))
            return PKCertificate(model.get('signer', None))

        else:
            # Invoke command with plain text output (to support
            # PKI Express < 1.3).
            self._invoke_plain(self.COMMAND_COMPLETE_SIG, args)


__all__ = ['SignatureFinisher']
