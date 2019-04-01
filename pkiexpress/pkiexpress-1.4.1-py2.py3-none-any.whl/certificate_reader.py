"""

Module that contains private-key certificate reader.

"""
import base64
import binascii
import json
import os

from .pk_certificate import PKCertificate
from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class CertificateReader(PkiExpressOperator):

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(CertificateReader, self).__init__(config)
        self.__cert_path = None

    @property
    def cert_path(self):
        return self.__cert_path

    # region set_cert

    def set_cert_from_path(self, path):
        if not path and not os.path.exists(path):
            raise Exception('The provided certificate file was not found')
        self.__cert_path = path

    def set_cert_from_raw(self, content_raw):
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__cert_path = temp_file_path

    def set_cert_from_base64(self, content_base64):
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided certificate is not Base64-encoded')
        self.set_cert_from_raw(raw)

    # endregion

    def decode(self):

        if not self.__cert_path or not os.path.exists(self.__cert_path):
            raise Exception('No certificate was provided')

        args = []
        if self.__cert_path:
            args.append('--file')
            args.append(self.__cert_path)

        # Invoke command.
        result = self._invoke(self.COMMAND_READ_CERT, args)

        # Parse output and return model.
        model = json.loads(base64.standard_b64decode(result[0]))
        return PKCertificate(model.get('info', None))


__all__ = ['CertificateReader']
