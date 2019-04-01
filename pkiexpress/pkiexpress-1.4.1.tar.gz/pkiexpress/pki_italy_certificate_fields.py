"""

Module that contains the class PkiItalyCertificateFields.

"""


class PkiItalyCertificateFields:

    def __init__(self, model):
        self.__certificate_type = model.get('certificateType')
        self.__codice_fiscale = model.get('codiceFiscale')
        self.__id_carta = model.get('idCarta')

    @property
    def certificate_type(self):
        return self.__certificate_type

    @certificate_type.setter
    def certificate_type(self, value):
        self.__certificate_type = value

    @property
    def codice_fiscale(self):
        return self.__codice_fiscale

    @codice_fiscale.setter
    def codice_fiscale(self, value):
        self.__codice_fiscale = value

    @property
    def id_carta(self):
        return self.__id_carta

    @id_carta.setter
    def id_carta(self, value):
        self.__id_carta = value


__all__ = ['PkiItalyCertificateFields']
