# coding: utf-8

"""
    Assetic Integration API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

##from assetic.models.assetic3_integration_representations_requestor_address import Assetic3IntegrationRepresentationsRequestorAddress  # noqa: F401,E501
##from assetic.models.assetic3_integration_representations_requestor_type_representation import Assetic3IntegrationRepresentationsRequestorTypeRepresentation  # noqa: F401,E501
##from assetic.models.web_api_hal_embedded_resource import WebApiHalEmbeddedResource  # noqa: F401,E501
##from assetic.models.web_api_hal_link import WebApiHalLink  # noqa: F401,E501


class Assetic3IntegrationRepresentationsRequestorRepresentation(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'display_name': 'str',
        'first_name': 'str',
        'surname': 'str',
        'company': 'str',
        'position': 'str',
        'phone': 'str',
        'mobile': 'str',
        'fax': 'str',
        'email': 'str',
        'address_comment': 'str',
        'external_id': 'str',
        'status_id': 'int',
        'status': 'str',
        'types': 'list[Assetic3IntegrationRepresentationsRequestorTypeRepresentation]',
        'address': 'Assetic3IntegrationRepresentationsRequestorAddress',
        'links': 'list[WebApiHalLink]',
        'embedded': 'list[WebApiHalEmbeddedResource]'
    }

    attribute_map = {
        'id': 'Id',
        'display_name': 'DisplayName',
        'first_name': 'FirstName',
        'surname': 'Surname',
        'company': 'Company',
        'position': 'Position',
        'phone': 'Phone',
        'mobile': 'Mobile',
        'fax': 'Fax',
        'email': 'Email',
        'address_comment': 'AddressComment',
        'external_id': 'ExternalID',
        'status_id': 'StatusId',
        'status': 'Status',
        'types': 'Types',
        'address': 'Address',
        'links': '_links',
        'embedded': '_embedded'
    }

    def __init__(self, id=None, display_name=None, first_name=None, surname=None, company=None, position=None, phone=None, mobile=None, fax=None, email=None, address_comment=None, external_id=None, status_id=None, status=None, types=None, address=None, links=None, embedded=None):  # noqa: E501
        """Assetic3IntegrationRepresentationsRequestorRepresentation - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._display_name = None
        self._first_name = None
        self._surname = None
        self._company = None
        self._position = None
        self._phone = None
        self._mobile = None
        self._fax = None
        self._email = None
        self._address_comment = None
        self._external_id = None
        self._status_id = None
        self._status = None
        self._types = None
        self._address = None
        self._links = None
        self._embedded = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if display_name is not None:
            self.display_name = display_name
        if first_name is not None:
            self.first_name = first_name
        if surname is not None:
            self.surname = surname
        if company is not None:
            self.company = company
        if position is not None:
            self.position = position
        if phone is not None:
            self.phone = phone
        if mobile is not None:
            self.mobile = mobile
        if fax is not None:
            self.fax = fax
        if email is not None:
            self.email = email
        if address_comment is not None:
            self.address_comment = address_comment
        if external_id is not None:
            self.external_id = external_id
        if status_id is not None:
            self.status_id = status_id
        if status is not None:
            self.status = status
        if types is not None:
            self.types = types
        if address is not None:
            self.address = address
        if links is not None:
            self.links = links
        if embedded is not None:
            self.embedded = embedded

    @property
    def id(self):
        """Gets the id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param id: The id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def display_name(self):
        """Gets the display_name of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The display_name of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param display_name: The display_name of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def first_name(self):
        """Gets the first_name of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The first_name of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param first_name: The first_name of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._first_name = first_name

    @property
    def surname(self):
        """Gets the surname of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The surname of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._surname

    @surname.setter
    def surname(self, surname):
        """Sets the surname of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param surname: The surname of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._surname = surname

    @property
    def company(self):
        """Gets the company of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The company of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._company

    @company.setter
    def company(self, company):
        """Sets the company of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param company: The company of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._company = company

    @property
    def position(self):
        """Gets the position of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The position of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param position: The position of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._position = position

    @property
    def phone(self):
        """Gets the phone of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The phone of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param phone: The phone of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def mobile(self):
        """Gets the mobile of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The mobile of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._mobile

    @mobile.setter
    def mobile(self, mobile):
        """Sets the mobile of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param mobile: The mobile of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._mobile = mobile

    @property
    def fax(self):
        """Gets the fax of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The fax of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._fax

    @fax.setter
    def fax(self, fax):
        """Sets the fax of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param fax: The fax of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._fax = fax

    @property
    def email(self):
        """Gets the email of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The email of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param email: The email of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def address_comment(self):
        """Gets the address_comment of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The address_comment of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._address_comment

    @address_comment.setter
    def address_comment(self, address_comment):
        """Sets the address_comment of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param address_comment: The address_comment of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._address_comment = address_comment

    @property
    def external_id(self):
        """Gets the external_id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The external_id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param external_id: The external_id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """

        self._external_id = external_id

    @property
    def status_id(self):
        """Gets the status_id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The status_id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: int
        """
        return self._status_id

    @status_id.setter
    def status_id(self, status_id):
        """Sets the status_id of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param status_id: The status_id of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: int
        """

        self._status_id = status_id

    @property
    def status(self):
        """Gets the status of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The status of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param status: The status of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: str
        """
        allowed_values = ["Active", "Inactive", "0", "1"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def types(self):
        """Gets the types of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The types of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: list[Assetic3IntegrationRepresentationsRequestorTypeRepresentation]
        """
        return self._types

    @types.setter
    def types(self, types):
        """Sets the types of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param types: The types of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: list[Assetic3IntegrationRepresentationsRequestorTypeRepresentation]
        """

        self._types = types

    @property
    def address(self):
        """Gets the address of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The address of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: Assetic3IntegrationRepresentationsRequestorAddress
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param address: The address of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: Assetic3IntegrationRepresentationsRequestorAddress
        """

        self._address = address

    @property
    def links(self):
        """Gets the links of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The links of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: list[WebApiHalLink]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param links: The links of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: list[WebApiHalLink]
        """

        self._links = links

    @property
    def embedded(self):
        """Gets the embedded of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501


        :return: The embedded of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :rtype: list[WebApiHalEmbeddedResource]
        """
        return self._embedded

    @embedded.setter
    def embedded(self, embedded):
        """Sets the embedded of this Assetic3IntegrationRepresentationsRequestorRepresentation.


        :param embedded: The embedded of this Assetic3IntegrationRepresentationsRequestorRepresentation.  # noqa: E501
        :type: list[WebApiHalEmbeddedResource]
        """

        self._embedded = embedded

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Assetic3IntegrationRepresentationsRequestorRepresentation, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Assetic3IntegrationRepresentationsRequestorRepresentation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
