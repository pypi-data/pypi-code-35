import os
import base64
import binascii

from abc import ABCMeta
from abc import abstractmethod

from .base_signer import BaseSigner
from .pki_express_config import PkiExpressConfig


class SignatureStarter(BaseSigner):
    __metaclass__ = ABCMeta

    def __init__(self, config):
        if not config:
            config = PkiExpressConfig()
        super(SignatureStarter, self).__init__(config)
        self._certificate_path = None

    # region set_certificate

    def set_certificate_from_path(self, path):
        if not os.path.exists(path):
            raise Exception('The provided certificate was not found')
        self._certificate_path = path

    def set_certificate_from_raw(self, content_raw):
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self._certificate_path = temp_file_path

    def set_certificate_from_base64(self, content_base64):
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided certificate is not Base64-encoded')

        self.set_certificate_from_raw(raw)

    # endregion

    @staticmethod
    def get_result(response, transfer_file):
        return {
            'toSignHash': response[0],
            'digestAlgorithm': response[1],
            'digestAlgorithmOid': response[2],
            'transferFile': transfer_file
        }

    @abstractmethod
    def start(self):
        raise Exception('This method should be implemented')


__all__ = ['SignatureStarter']
