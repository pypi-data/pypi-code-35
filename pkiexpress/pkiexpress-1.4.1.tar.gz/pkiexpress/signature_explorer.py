import base64
import binascii
import os

from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class SignatureExplorer(PkiExpressOperator):

    def __init__(self, config=None):
        if config is None:
            config = PkiExpressConfig()
        super(SignatureExplorer, self).__init__(config)

        self._signature_file_path = None
        self._validate = None

    @property
    def signature_file_path(self):
        return self._signature_file_path

    # region set_signature_file

    def set_signature_file_from_path(self, path):
        """

        Sets the path of the signature file to be opened.
        :param path: The path of the signature to be opened.

        """
        if not os.path.exists(path):
            raise Exception('The provided signature file to opened was not '
                            'found')
        self._signature_file_path = path

    def set_signature_file_from_raw(self, content_raw):
        """

        Sets the content of the signature file to be opened.
        :param content_raw: The content of the signature file to be opened.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self._signature_file_path = temp_file_path

    def set_signature_file_from_base64(self, content_base64):
        """

        Sets the base64-encoded content of the signature file to be opened.
        :param content_base64: The base64-encoded content of the signature file
                               to be opened.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided file to be signed is not '
                            'base64-encoded')
        self.set_signature_file_from_raw(raw)

    # endregion

    @property
    def validate(self):
        return self._validate

    @validate.setter
    def validate(self, value):
        self._validate = value


__all__ = ['SignatureExplorer']
