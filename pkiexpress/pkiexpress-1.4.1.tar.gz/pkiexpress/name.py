"""

Module that contains the class of a X.509 name.

"""

class Name(object):
    """

    Class the represents a X.509 name.

    """

    def __init__(self, model):
        self.__country = model.get('country', None)
        self.__organization = model.get('organization', None)
        self.__organization_unit = model.get('organizationUnit', None)
        self.__dn_qualifier = model.get('dnQualifier', None)
        self.__state_name = model.get('stateName', None)
        self.__common_name = model.get('commonName', None)
        self.__serial_number = model.get('serialNumber', None)
        self.__locality = model.get('locality', None)
        self.__title = model.get('title', None)
        self.__surname = model.get('surname', None)
        self.__given_name = model.get('givenName', None)
        self.__initials = model.get('initials', None)
        self.__pseudonym = model.get('pseudonym', None)
        self.__generation_qualifier = model.get('generationQualifier', None)
        self.__email_address = model.get('emailAddress', None)

    @property
    def country(self):
        return self.__country

    @country.setter
    def country(self, value):
        self.__country = value

    @property
    def organization(self):
        return self.__organization

    @organization.setter
    def organization(self, value):
        self.__organization = value

    @property
    def organization_unit(self):
        return self.__organization_unit

    @organization_unit.setter
    def organization_unit(self, value):
        self.__organization_unit = value

    @property
    def dn_qualifier(self):
        return self.__dn_qualifier

    @dn_qualifier.setter
    def dn_qualifier(self, value):
        self.__dn_qualifier = value

    @property
    def state_name(self):
        return self.__state_name

    @state_name.setter
    def state_name(self, value):
        self.__state_name = value

    @property
    def common_name(self):
        return self.__common_name

    @common_name.setter
    def common_name(self, value):
        self.__common_name = value

    @property
    def serial_number(self):
        return self.__serial_number

    @serial_number.setter
    def serial_number(self, value):
        self.__serial_number = value

    @property
    def locality(self):
        return self.__locality

    @locality.setter
    def locality(self, value):
        self.__locality = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        self.__surname = value

    @property
    def given_name(self):
        return self.__given_name

    @given_name.setter
    def given_name(self, value):
        self.__given_name = value

    @property
    def initials(self):
        return self.__initials

    @initials.setter
    def initials(self, value):
        self.__initials = value

    @property
    def pseudonym(self):
        return self.__pseudonym

    @pseudonym.setter
    def pseudonym(self, value):
        self.__pseudonym = value

    @property
    def generation_qualifier(self):
        return self.__generation_qualifier

    @generation_qualifier.setter
    def generation_qualifier(self, value):
        self.__generation_qualifier = value

    @property
    def email_address(self):
        return self.__email_address

    @email_address.setter
    def email_address(self, value):
        self.__email_address = value


__all__ = ['Name']
