"""

Module containing the CAdES signer class.

"""
import base64
import binascii
import json
import os

from .pk_certificate import PKCertificate
from .signer import Signer
from .pki_express_config import PkiExpressConfig


class CadesSigner(Signer):
    """

    Class performs a local CAdES signature.

    """

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(CadesSigner, self).__init__(config)
        self.__file_to_sign_path = None
        self.__data_file_path = None
        self.__encapsulate_content = True

    # region set_file_to_sign

    def set_file_to_sign_from_path(self, path):
        """

        Sets the file to be signed from its path.
        :param path: The path of the file to be signed.

        """
        if not os.path.exists(path):
            raise Exception('The provided file to be signed was not found')
        self.__file_to_sign_path = path

    def set_file_to_sign_from_raw(self, content_raw):
        """

        Sets the file to be signed from its binary content.
        :param content_raw: The binary content of the file to be signed.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__file_to_sign_path = temp_file_path

    def set_file_to_sign_from_base64(self, content_base64):
        """

        Sets the file  to be signed from its Base64-encoded content.
        :param content_base64: The Base64-encoded content of the file to be
                               signed.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided file to be signed is not '
                            'Base64-encoded')
        self.set_file_to_sign_from_raw(raw)

    # endregion

    # region set_data_file

    def set_data_file_from_path(self, path):
        """

        Sets the data file from its path.
        :param path: The path to the data file.

        """
        if not os.path.exists(path):
            raise Exception('The provided data file was not found')
        self.__data_file_path = path

    def set_data_file_from_raw(self, content_raw):
        """

        Sets the data file from its binary content.
        :param content_raw: The binary content of the data file.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__data_file_path = temp_file_path

    def set_data_file_from_base64(self, content_base64):
        """

        Sets the data file from its Base64-encoded content.
        :param content_base64: The Base64-encoded content of the data file.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided data file to be signed is not '
                            'Base64-encoded')
        self.set_data_file_from_raw(raw)

    # endregion

    def sign(self, get_cert=False):
        """

        Performs a CAdES signature.

        """
        if not self.__file_to_sign_path:
            raise Exception('The file to be signed was not set')

        if not self._output_file_path:
            raise Exception('The output destination was not set')

        args = [
            self.__file_to_sign_path,
            self._output_file_path
        ]

        # Verify and add common options between signers
        self._verify_and_add_common_options(args)

        if self.__data_file_path:
            args.append('--data-file')
            args.append(self.__data_file_path)

        if not self.__encapsulate_content:
            args.append('--detached')

        if get_cert:
            # This operation can only be used on version greater than 1.8 of the
            # PKI Express.
            self._version_manager.require_version('1.8')

            # Invoke command.
            result = self._invoke(self.COMMAND_SIGN_CADES, args)

            # Parse output and return model.
            model = json.loads(base64.standard_b64decode(result[0]))
            return PKCertificate(model.get('signer', None))

        else:
            # Invoke command with plain text output (to support
            # PKI Express < 1.3).
            self._invoke_plain(self.COMMAND_SIGN_CADES, args)

    @property
    def encapsulated_content(self):
        """

        Property for the "encapsulate content" permission.
        :return: The permission to "encapsulate content"

        """
        return self.__encapsulate_content

    @encapsulated_content.setter
    def encapsulated_content(self, value):
        self.__encapsulate_content = value


__all__ = ['CadesSigner']
