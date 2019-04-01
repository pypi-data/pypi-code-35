"""

Module containing CadesSignatureEditor class.

"""
import base64
import binascii
import os

from .pki_express_config import PkiExpressConfig
from .pki_express_operator import PkiExpressOperator


class CadesSignatureEditor(PkiExpressOperator):

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(CadesSignatureEditor, self).__init__(config)
        self.__output_file_path = None
        self.__data_file_path = None
        self.__encapsulate_content = True
        self.__cms_files = []

    @property
    def data_file_path(self):
        return self.__data_file_path

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

    @property
    def output_file(self):
        return self.__output_file_path

    @output_file.setter
    def output_file(self, value):
        self.__output_file_path = value

    @property
    def cms_files(self):
        return self.__cms_files

    # region add_cms_file

    def add_cms_file_from_path(self, path):
        """

        Adds a CMS file from its path.
        :param: path: The path of the CMS file.

        """
        if not os.path.exists(path):
            raise Exception('The provided data file was not found')
        self.__cms_files.append(path)

    def add_cms_file_from_raw(self, content_raw):
        """

        Adds a CMS file from its binary content.
        :param content_raw: The binary content of the CMS file.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__cms_files.append(temp_file_path)

    def add_cms_file_from_base64(self, content_base64):
        """

        Adds a CMS file from its Base64-encoded content.
        :param content_base64: The Base64-encoded content of the CMS file.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided cms file to be merged is not '
                            'Base64-encoded')
        self.add_cms_file_from_raw(raw)

    # endregion

    @property
    def encapsulate_content(self):
        return self.__encapsulate_content

    @encapsulate_content.setter
    def encapsulate_content(self, value):
        self.__encapsulate_content = value

    def merge(self):

        if not self.__cms_files:
            raise Exception('The CMS/CAdES files was not set')

        if len(self.__cms_files) < 2:
            raise Exception('Insufficient CMS/CAdES files for merging. '
                            'Provided at least two signatures.')

        if not self.__output_file_path:
            raise Exception('The output destination was not set')

        args = [ self.__output_file_path ]
        args.extend(self.__cms_files)

        if self.__data_file_path:
            args.append('--data-file')
            args.append(self.__data_file_path)

        if not self.__encapsulate_content:
            args.append('--detached')

        self._version_manager.require_version('1.9')

        # Invoke command.
        self._invoke(self.COMMAND_MERGE_CMS, args)


__all__ = ['CadesSignatureEditor']
