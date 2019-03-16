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


class TopicL1RespModel(object):
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
        'topic': 'str',
        'keywords_weight': 'list[str]',
        'strength': 'str',
        'doc_topic_exposure': 'list[str]',
        'doc_id': 'list[str]'
    }

    attribute_map = {
        'topic': 'topic',
        'keywords_weight': 'keywords_weight',
        'strength': 'strength',
        'doc_topic_exposure': 'doc_topic_exposure',
        'doc_id': 'doc_id'
    }

    def __init__(self, topic=None, keywords_weight=None, strength=None, doc_topic_exposure=None, doc_id=None):  # noqa: E501
        """TopicL1RespModel - a model defined in Swagger"""  # noqa: E501

        self._topic = None
        self._keywords_weight = None
        self._strength = None
        self._doc_topic_exposure = None
        self._doc_id = None
        self.discriminator = None

        if topic is not None:
            self.topic = topic
        if keywords_weight is not None:
            self.keywords_weight = keywords_weight
        if strength is not None:
            self.strength = strength
        if doc_topic_exposure is not None:
            self.doc_topic_exposure = doc_topic_exposure
        if doc_id is not None:
            self.doc_id = doc_id

    @property
    def topic(self):
        """Gets the topic of this TopicL1RespModel.  # noqa: E501

        Topic  # noqa: E501

        :return: The topic of this TopicL1RespModel.  # noqa: E501
        :rtype: str
        """
        return self._topic

    @topic.setter
    def topic(self, topic):
        """Sets the topic of this TopicL1RespModel.

        Topic  # noqa: E501

        :param topic: The topic of this TopicL1RespModel.  # noqa: E501
        :type: str
        """

        self._topic = topic

    @property
    def keywords_weight(self):
        """Gets the keywords_weight of this TopicL1RespModel.  # noqa: E501


        :return: The keywords_weight of this TopicL1RespModel.  # noqa: E501
        :rtype: list[str]
        """
        return self._keywords_weight

    @keywords_weight.setter
    def keywords_weight(self, keywords_weight):
        """Sets the keywords_weight of this TopicL1RespModel.


        :param keywords_weight: The keywords_weight of this TopicL1RespModel.  # noqa: E501
        :type: list[str]
        """

        self._keywords_weight = keywords_weight

    @property
    def strength(self):
        """Gets the strength of this TopicL1RespModel.  # noqa: E501

        Prevalence of each topic in the dataset  # noqa: E501

        :return: The strength of this TopicL1RespModel.  # noqa: E501
        :rtype: str
        """
        return self._strength

    @strength.setter
    def strength(self, strength):
        """Sets the strength of this TopicL1RespModel.

        Prevalence of each topic in the dataset  # noqa: E501

        :param strength: The strength of this TopicL1RespModel.  # noqa: E501
        :type: str
        """

        self._strength = strength

    @property
    def doc_topic_exposure(self):
        """Gets the doc_topic_exposure of this TopicL1RespModel.  # noqa: E501


        :return: The doc_topic_exposure of this TopicL1RespModel.  # noqa: E501
        :rtype: list[str]
        """
        return self._doc_topic_exposure

    @doc_topic_exposure.setter
    def doc_topic_exposure(self, doc_topic_exposure):
        """Sets the doc_topic_exposure of this TopicL1RespModel.


        :param doc_topic_exposure: The doc_topic_exposure of this TopicL1RespModel.  # noqa: E501
        :type: list[str]
        """

        self._doc_topic_exposure = doc_topic_exposure

    @property
    def doc_id(self):
        """Gets the doc_id of this TopicL1RespModel.  # noqa: E501


        :return: The doc_id of this TopicL1RespModel.  # noqa: E501
        :rtype: list[str]
        """
        return self._doc_id

    @doc_id.setter
    def doc_id(self, doc_id):
        """Sets the doc_id of this TopicL1RespModel.


        :param doc_id: The doc_id of this TopicL1RespModel.  # noqa: E501
        :type: list[str]
        """

        self._doc_id = doc_id

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
        if issubclass(TopicL1RespModel, dict):
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
        if not isinstance(other, TopicL1RespModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
