"""

Module containing the PAdES timestamper.

"""
import base64
import binascii
import os

from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class PadesTimestamper(PkiExpressOperator):
    """

    Class that adds a timestamper to PDF file.

    """

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(PadesTimestamper, self).__init__(config)
        self.__pdf_path = None
        self.__output_file_path = None
        self.__overwrite_original_file = False

    @property
    def pdf_path(self):
        """

        Gets the path of the PDF to be timestamped.
        :return: The path of the PDF to be timestamped.

        """
        return self.__pdf_path

    # region set_pdf

    def set_pdf_from_path(self, path):
        """

        Sets the PDF to be timestamped from its path.
        :param path: The path of the PDF to be timestamped.

        """
        if not os.path.exists(path):
            raise Exception('The provided PDF was not found')
        self.__pdf_path = path

    def set_pdf_from_raw(self, content_raw):
        """

        Sets the PDF to be timestamped from its content.
        :param content_raw: The content of the PDF to be timestamped.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__pdf_path = temp_file_path

    def set_pdf_from_base64(self, content_base64):
        """

        Sets the PDF to be timestamped from its Base64-encoded content.
        :param content_base64: The Base64-encoded content of the PDF to be
                               timestamped.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided PDF is not Base64-encoded')
        self.set_pdf_from_raw(raw)

    # endregion

    @property
    def output_file_path(self):
        """

        Gets the path where the output file will be stored.
        :return: The path where the output file will be stored.

        """
        return self.__output_file_path

    @output_file_path.setter
    def output_file_path(self, value):
        """

        Sets the path where the output file will be stored.
        :param value: The path where the output file will be stored.

        """
        self.__output_file_path = value

    @property
    def overwrite_original_file(self):
        """

        Gets the value of the "Overwrite original file" option.
        :return: The value of the "Overwrite original file" option.

        """
        return self.__overwrite_original_file

    @overwrite_original_file.setter
    def overwrite_original_file(self, value):
        """

        Sets the value of the "Overwrite original file" option.
        :param value: The value of the "Overwrite original file" option.

        """
        self.__overwrite_original_file = value

    def stamp(self):
        """

        Perform the timestamp on the PDF file.

        """
        if not self.__pdf_path:
            raise Exception('The PDF to be timestamped was not set')

        if not self.__overwrite_original_file and not self.__output_file_path:
            raise Exception("The output destination was not set")

        args = [self.__pdf_path]

        # Add timestamp authority.
        if self._timestamp_authority:
            self._timestamp_authority\
                .add_cmd_arguments(args, self._version_manager)

            # This option can only be used on versions greater then 1.5 of the
            # PKI Express.
            self._version_manager.require_version('1.5')

        # Logic to overwrite original file or use the output file.
        if self.__overwrite_original_file:
            args.append('--overwrite')
        else:
            args.append(self.__output_file_path)

        # This operation can only be used on versions greater than 1.7 of the
        # PKI Express.
        self._version_manager.require_version('1.7')

        # Invoke command.
        self._invoke(self.COMMAND_STAMP_PDF, args)


__all__ = ['PadesTimestamper']
