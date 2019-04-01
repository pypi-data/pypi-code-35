"""

Module that contains the class PkiBrazilCertificateFields.

"""
import re


class PkiBrazilCertificateFields:

    def __init__(self, model):
        self.__certificate_type = model.get('certificateType', None)
        self.__cpf = model.get('cpf', None)
        self.__cnpj = model.get('cnpj', None)
        self.__responsavel = model.get('responsavel', None)
        self.__date_of_birth = model.get('dateOfBirth', None)
        self.__company_name = model.get('companyName', None)
        self.__rg_numero = model.get('rgNumero', None)
        self.__rg_emissor = model.get('rgEmissor', None)
        self.__rg_emissor_uf = model.get('rgEmissorUF', None)
        self.__oab_numero = model.get('oabNumero', None)
        self.__oab_uf = model.get('oabUF', None)

    @property
    def certificate_type(self):
        return self.__certificate_type

    @certificate_type.setter
    def certificate_type(self, value):
        self.__certificate_type = value

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, value):
        self.__cpf = value

    @property
    def cpf_formatted(self):
        if self.__cpf is None:
            return ''
        if not re.match('^\d{11}$', self.__cpf):
            return self.__cpf
        return "%s.%s.%s-%s" % (self.__cpf[:3], self.__cpf[3:6],
                                self.__cpf[6:9], self.__cpf[9:])

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, value):
        self.__cnpj = value

    @property
    def cnpj_formatted(self):
        if self.__cnpj is None:
            return ''
        if not re.match('^\d{14}$', self.__cnpj):
            return self.__cnpj
        return "%s.%s.%s/%s-%s" % (self.__cnpj[:2], self.__cnpj[2:5],
                                   self.__cnpj[5:8], self.__cnpj[8:12],
                                   self.__cnpj[12:])

    @property
    def responsavel(self):
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, value):
        self.__responsavel = value

    @property
    def company_name(self):
        return self.__company_name

    @company_name.setter
    def company_name(self, value):
        self.__company_name = value

    @property
    def oab_uf(self):
        return self.__oab_uf

    @oab_uf.setter
    def oab_uf(self, value):
        self.__oab_uf = value

    @property
    def oab_numero(self):
        return self.__oab_numero

    @oab_numero.setter
    def oab_numero(self, value):
        self.__oab_numero = value

    @property
    def rg_numero(self):
        return self.__rg_numero

    @rg_numero.setter
    def rg_numero(self, value):
        self.__rg_numero = value

    @property
    def rg_emissor(self):
        return self.__rg_emissor

    @rg_emissor.setter
    def rg_emissor(self, value):
        self.__rg_emissor = value

    @property
    def rg_emissor_uf(self):
        return self.__rg_emissor_uf

    @rg_emissor_uf.setter
    def rg_emissor_uf(self, value):
        self.__rg_emissor_uf = value

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        self.__date_of_birth = value


__all__ = ['PkiBrazilCertificateFields']
