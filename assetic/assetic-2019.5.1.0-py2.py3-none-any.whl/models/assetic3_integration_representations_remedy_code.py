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

##from assetic.models.web_api_hal_embedded_resource import WebApiHalEmbeddedResource  # noqa: F401,E501
##from assetic.models.web_api_hal_link import WebApiHalLink  # noqa: F401,E501


class Assetic3IntegrationRepresentationsRemedyCode(object):
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
        'id': 'int',
        'description': 'str',
        'code_number': 'str',
        'activity': 'str',
        'links': 'list[WebApiHalLink]',
        'embedded': 'list[WebApiHalEmbeddedResource]'
    }

    attribute_map = {
        'id': 'Id',
        'description': 'Description',
        'code_number': 'CodeNumber',
        'activity': 'Activity',
        'links': '_links',
        'embedded': '_embedded'
    }

    def __init__(self, id=None, description=None, code_number=None, activity=None, links=None, embedded=None):  # noqa: E501
        """Assetic3IntegrationRepresentationsRemedyCode - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._description = None
        self._code_number = None
        self._activity = None
        self._links = None
        self._embedded = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if description is not None:
            self.description = description
        if code_number is not None:
            self.code_number = code_number
        if activity is not None:
            self.activity = activity
        if links is not None:
            self.links = links
        if embedded is not None:
            self.embedded = embedded

    @property
    def id(self):
        """Gets the id of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501


        :return: The id of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Assetic3IntegrationRepresentationsRemedyCode.


        :param id: The id of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def description(self):
        """Gets the description of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501


        :return: The description of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Assetic3IntegrationRepresentationsRemedyCode.


        :param description: The description of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def code_number(self):
        """Gets the code_number of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501


        :return: The code_number of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :rtype: str
        """
        return self._code_number

    @code_number.setter
    def code_number(self, code_number):
        """Sets the code_number of this Assetic3IntegrationRepresentationsRemedyCode.


        :param code_number: The code_number of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :type: str
        """

        self._code_number = code_number

    @property
    def activity(self):
        """Gets the activity of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501


        :return: The activity of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :rtype: str
        """
        return self._activity

    @activity.setter
    def activity(self, activity):
        """Sets the activity of this Assetic3IntegrationRepresentationsRemedyCode.


        :param activity: The activity of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :type: str
        """

        self._activity = activity

    @property
    def links(self):
        """Gets the links of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501


        :return: The links of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :rtype: list[WebApiHalLink]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Assetic3IntegrationRepresentationsRemedyCode.


        :param links: The links of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :type: list[WebApiHalLink]
        """

        self._links = links

    @property
    def embedded(self):
        """Gets the embedded of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501


        :return: The embedded of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
        :rtype: list[WebApiHalEmbeddedResource]
        """
        return self._embedded

    @embedded.setter
    def embedded(self, embedded):
        """Sets the embedded of this Assetic3IntegrationRepresentationsRemedyCode.


        :param embedded: The embedded of this Assetic3IntegrationRepresentationsRemedyCode.  # noqa: E501
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
        if issubclass(Assetic3IntegrationRepresentationsRemedyCode, dict):
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
        if not isinstance(other, Assetic3IntegrationRepresentationsRemedyCode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
