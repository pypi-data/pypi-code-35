"""

Module containing the PKI Express configuration class.

"""
import os
import tempfile


class PkiExpressConfig(object):
    """

    Contains configuration about the use of PKI Express on this library.

    """

    def __init__(self, pki_express_home=None, temp_folder=None,
                 transfer_data_folder=None):

        if temp_folder is not None and os.path.exists(temp_folder):
            self.__temp_folder = temp_folder
        else:
            self.__temp_folder = tempfile.gettempdir()

        if transfer_data_folder is not None and \
                os.path.exists(transfer_data_folder):
            self.__transfer_data_folder = transfer_data_folder
        else:
            self.__transfer_data_folder = self.__temp_folder

        self.__pki_express_home = pki_express_home

    @property
    def pki_express_home(self):
        """

        Gets the PKI Express's home path.
        :return: PKI Express's home path.

        """
        return self.__pki_express_home

    @property
    def temp_folder(self):
        """

        Gets this library's temp folder.
        :return: This library's temp folder.

        """
        return self.__temp_folder

    @property
    def transfer_data_folder(self):
        """

        Gets this library's folder where all transfer data files will be stored.
        :return: This library's transfer data folder.

        """
        return self.__transfer_data_folder


__all__ = ['PkiExpressConfig']
