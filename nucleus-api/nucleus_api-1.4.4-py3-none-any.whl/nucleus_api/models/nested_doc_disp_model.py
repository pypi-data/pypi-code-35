# coding: utf-8

"""
    Nucleus API

    Nucleus text analytics APIs from SumUp Analytics. Example and documentation: https://github.com/SumUpAnalytics/nucleus-sdk  # noqa: E501

    OpenAPI spec version: v1.4.4
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class NestedDocDispModel(object):
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
        'title': 'str',
        'sourceid': 'str',
        'content': 'str',
        'attribute': 'object'
    }

    attribute_map = {
        'title': 'title',
        'sourceid': 'sourceid',
        'content': 'content',
        'attribute': 'attribute'
    }

    def __init__(self, title=None, sourceid=None, content=None, attribute=None):  # noqa: E501
        """NestedDocDispModel - a model defined in Swagger"""  # noqa: E501

        self._title = None
        self._sourceid = None
        self._content = None
        self._attribute = None
        self.discriminator = None

        if title is not None:
            self.title = title
        if sourceid is not None:
            self.sourceid = sourceid
        if content is not None:
            self.content = content
        if attribute is not None:
            self.attribute = attribute

    @property
    def title(self):
        """Gets the title of this NestedDocDispModel.  # noqa: E501

        Document title  # noqa: E501

        :return: The title of this NestedDocDispModel.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this NestedDocDispModel.

        Document title  # noqa: E501

        :param title: The title of this NestedDocDispModel.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def sourceid(self):
        """Gets the sourceid of this NestedDocDispModel.  # noqa: E501

        Document ID  # noqa: E501

        :return: The sourceid of this NestedDocDispModel.  # noqa: E501
        :rtype: str
        """
        return self._sourceid

    @sourceid.setter
    def sourceid(self, sourceid):
        """Sets the sourceid of this NestedDocDispModel.

        Document ID  # noqa: E501

        :param sourceid: The sourceid of this NestedDocDispModel.  # noqa: E501
        :type: str
        """

        self._sourceid = sourceid

    @property
    def content(self):
        """Gets the content of this NestedDocDispModel.  # noqa: E501

        Document content  # noqa: E501

        :return: The content of this NestedDocDispModel.  # noqa: E501
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """Sets the content of this NestedDocDispModel.

        Document content  # noqa: E501

        :param content: The content of this NestedDocDispModel.  # noqa: E501
        :type: str
        """

        self._content = content

    @property
    def attribute(self):
        """Gets the attribute of this NestedDocDispModel.  # noqa: E501

        JSON containing document metadata key:value pairs (eg. author, time..)  # noqa: E501

        :return: The attribute of this NestedDocDispModel.  # noqa: E501
        :rtype: object
        """
        return self._attribute

    @attribute.setter
    def attribute(self, attribute):
        """Sets the attribute of this NestedDocDispModel.

        JSON containing document metadata key:value pairs (eg. author, time..)  # noqa: E501

        :param attribute: The attribute of this NestedDocDispModel.  # noqa: E501
        :type: object
        """

        self._attribute = attribute

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
        if issubclass(NestedDocDispModel, dict):
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
        if not isinstance(other, NestedDocDispModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
