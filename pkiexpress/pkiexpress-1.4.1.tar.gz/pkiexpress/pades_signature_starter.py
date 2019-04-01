"""

Module containing PadesSignatureStarter class.

"""
import base64
import binascii
import json
import os

from .pki_express_config import PkiExpressConfig
from .signature_starter import SignatureStarter


class PadesSignatureStarter(SignatureStarter):
    """

    Class that performs the initialization of a PAdES signature.

    """

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(PadesSignatureStarter, self).__init__(config)
        self.__pdf_to_sign_path = None
        self.__vr_json_path = None

    # region set_pdf_to_sign

    def set_pdf_to_sign_from_path(self, path):
        """

        Sets the PDF to be signed from its path.
        :param path: The path of the PDF to be signed.

        """
        if not os.path.exists(path):
            raise Exception('The provided PDF to be signed was not found')
        self.__pdf_to_sign_path = path

    def set_pdf_to_sign_from_raw(self, content_raw):
        """

        Sets the PDF to be signed from its content.
        :param content_raw: The content of the PDF to be signed.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__pdf_to_sign_path = temp_file_path

    def set_pdf_to_sign_from_base64(self, content_base64):
        """

        Sets the PDF to be signed from its Base64-encoded content.
        :param content_base64: The Base64-encoded content of the the PDF to be
                               signed.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided PDF to be signed iw not '
                            'Base64-encoded')
        self.set_pdf_to_sign_from_raw(raw)

    # endregion

    # region set_visual_representation

    def set_visual_representation_file(self, path):
        """

        Sets the visual representation for the signature from a JSON file.
        :param path: Path of the JSON file that represents the visual
                     representation.

        """
        if not os.path.exists(path):
            raise Exception('The provided visual representation file was not '
                            'found')
        self.__vr_json_path = path

    def set_visual_representation(self, representation):
        """

        Sets the visual representation for the signature from a model.
        :param representation: The model of the visual representation.

        """
        try:
            json_str = json.dumps(representation)
        except TypeError:
            raise Exception('The provided visual representation, was not valid')
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'w') as file_desc:
            file_desc.write(json_str)
        self.__vr_json_path = temp_file_path

    # endregion

    def start(self):
        """

        Starts a PAdES signature.
        :return: The result of the signature init. These values are used by
                 SignatureFinisher.

        """
        if not self.__pdf_to_sign_path:
            raise Exception('The PDF to be signed was not set')

        if not self._certificate_path:
            raise Exception('The certificate was not set')

        # Generate transfer file
        transfer_file = self.get_transfer_file_name()

        args = [
            self.__pdf_to_sign_path,
            self._certificate_path,
            os.path.join(self._config.transfer_data_folder, transfer_file)
        ]

        # Verify and add common options between signers
        self._verify_and_add_common_options(args)

        if self.__vr_json_path:
            args.append('--visual-rep')
            args.append(self.__vr_json_path)

        # Invoke command with plain text output (to support PKI Express < 1.3)
        response = self._invoke_plain(self.COMMAND_START_PADES, args)
        return self.get_result(response, transfer_file)


__all__ = ['PadesSignatureStarter']
