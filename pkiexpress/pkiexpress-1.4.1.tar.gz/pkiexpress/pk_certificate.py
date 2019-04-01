"""

Module containing the model for a private-key certificate.

"""
import base64

from .name import Name
from .pki_brazil_certificate_fields import PkiBrazilCertificateFields
from .pki_italy_certificate_fields import PkiItalyCertificateFields


class PKCertificate(object):
    """

    Class that represents a private-key certificate.

    """

    def __init__(self, model):

        self.__subject_name = None
        self.__email_address = None
        self.__issuer_name = None
        self.__serial_number = None
        self.__validity_start = None
        self.__validity_end = None
        self.__pki_brazil = None
        self.__pki_italy = None
        self.__issuer = None
        self.__binary_thumbprint_sha256 = None

        if model is not None:
            self.__email_address = model.get('emailAddress', None)
            self.__issuer_display_name = model.get('issuerDisplayName', None)
            self.__serial_number = model.get('serialNumber', None)
            self.__thumbprint = model.get('thumbprint', None)
            self.__validity_start = model.get('validityStart', None)
            self.__validity_end = model.get('validityEnd', None)

            if model.get('subjectName', None) is not None:
                self.__subject_name = Name(model.get('subjectName'))

            if model.get('issuerName', None) is not None:
                self.__issuer_name = Name(model.get('issuerName'))

            if model.get('pkiBrazil', None) is not None:
                self.__pki_brazil = PkiBrazilCertificateFields(
                    model.get('pkiBrazil'))

            if model.get('pkiItaly', None) is not None:
                self.__pki_italy = PkiItalyCertificateFields(
                    model.get('pkiItaly'))

            if model.get('issuer', None) is not None:
                self.__issuer = PKCertificate(model.get('issuer'))

            if model.get('binaryThumbprintSHA256', None) is not None:
                self.__binary_thumbprint_sha256 = base64.standard_b64decode(
                    model.get('binaryThumbprintSHA256'))

    @property
    def subject_name(self):
        return self.__subject_name

    @subject_name.setter
    def subject_name(self, value):
        self.__subject_name = value

    @property
    def email_address(self):
        return self.__email_address

    @email_address.setter
    def email_address(self, value):
        self.__email_address = value

    @property
    def issuer_name(self):
        return self.__issuer_name

    @issuer_name.setter
    def issuer_name(self, value):
        self.__issuer_name = value

    @property
    def serial_number(self):
        return self.__serial_number

    @serial_number.setter
    def serial_number(self, value):
        self.__serial_number = value

    @property
    def validity_start(self):
        return self.__validity_start

    @validity_start.setter
    def validity_start(self, value):
        self.__validity_start = value

    @property
    def validity_end(self):
        return self.__validity_end

    @validity_end.setter
    def validity_end(self, value):
        self.__validity_end = value

    @property
    def pki_brazil(self):
        return self.__pki_brazil

    @pki_brazil.setter
    def pki_brazil(self, value):
        self.__pki_brazil = value

    @property
    def pki_italy(self):
        return self.__pki_italy

    @pki_italy.setter
    def pki_italy(self, value):
        self.__pki_italy = value

    @property
    def issuer(self):
        return self.__issuer

    @issuer.setter
    def issuer(self, value):
        self.__issuer = value

    @property
    def binary_thumbprint_sha256(self):
        return self.__binary_thumbprint_sha256

    @binary_thumbprint_sha256.setter
    def binary_thumbprint_sha256(self, value):
        self.__binary_thumbprint_sha256 = value

    @property
    def thumbprint(self):
        return self.__thumbprint

    @thumbprint.setter
    def thumbprint(self, value):
        self.__thumbprint = value


__all__ = ['PKCertificate']
