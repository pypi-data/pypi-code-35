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


class NestedSummaryModel(object):
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
        'sentences': 'str',
        'sourceid': 'str',
        'attribute': 'object'
    }

    attribute_map = {
        'title': 'title',
        'sentences': 'sentences',
        'sourceid': 'sourceid',
        'attribute': 'attribute'
    }

    def __init__(self, title=None, sentences=None, sourceid=None, attribute=None):  # noqa: E501
        """NestedSummaryModel - a model defined in Swagger"""  # noqa: E501

        self._title = None
        self._sentences = None
        self._sourceid = None
        self._attribute = None
        self.discriminator = None

        if title is not None:
            self.title = title
        if sentences is not None:
            self.sentences = sentences
        if sourceid is not None:
            self.sourceid = sourceid
        if attribute is not None:
            self.attribute = attribute

    @property
    def title(self):
        """Gets the title of this NestedSummaryModel.  # noqa: E501

        Document Title  # noqa: E501

        :return: The title of this NestedSummaryModel.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this NestedSummaryModel.

        Document Title  # noqa: E501

        :param title: The title of this NestedSummaryModel.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def sentences(self):
        """Gets the sentences of this NestedSummaryModel.  # noqa: E501

        Sentences  # noqa: E501

        :return: The sentences of this NestedSummaryModel.  # noqa: E501
        :rtype: str
        """
        return self._sentences

    @sentences.setter
    def sentences(self, sentences):
        """Sets the sentences of this NestedSummaryModel.

        Sentences  # noqa: E501

        :param sentences: The sentences of this NestedSummaryModel.  # noqa: E501
        :type: str
        """

        self._sentences = sentences

    @property
    def sourceid(self):
        """Gets the sourceid of this NestedSummaryModel.  # noqa: E501

        Document ID  # noqa: E501

        :return: The sourceid of this NestedSummaryModel.  # noqa: E501
        :rtype: str
        """
        return self._sourceid

    @sourceid.setter
    def sourceid(self, sourceid):
        """Sets the sourceid of this NestedSummaryModel.

        Document ID  # noqa: E501

        :param sourceid: The sourceid of this NestedSummaryModel.  # noqa: E501
        :type: str
        """

        self._sourceid = sourceid

    @property
    def attribute(self):
        """Gets the attribute of this NestedSummaryModel.  # noqa: E501

        JSON containing document metadata key:value pairs (eg. author, time..)  # noqa: E501

        :return: The attribute of this NestedSummaryModel.  # noqa: E501
        :rtype: object
        """
        return self._attribute

    @attribute.setter
    def attribute(self, attribute):
        """Sets the attribute of this NestedSummaryModel.

        JSON containing document metadata key:value pairs (eg. author, time..)  # noqa: E501

        :param attribute: The attribute of this NestedSummaryModel.  # noqa: E501
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
        if issubclass(NestedSummaryModel, dict):
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
        if not isinstance(other, NestedSummaryModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
