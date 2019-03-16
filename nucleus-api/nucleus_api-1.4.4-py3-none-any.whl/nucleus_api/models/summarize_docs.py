# coding: utf-8

"""
    Nucleus API

    Nucleus text analytics APIs from SumUp Analytics. Example and documentation: https://github.com/SumUpAnalytics/nucleus-sdk  # noqa: E501

    OpenAPI spec version: v1.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class SummarizeDocs(object):
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
        'dataset': 'str',
        'doc_title': 'str',
        'custom_stop_words': 'list[str]',
        'summary_length': 'int',
        'context_amount': 'int',
        'short_sentence_length': 'int',
        'long_sentence_length': 'int'
    }

    attribute_map = {
        'dataset': 'dataset',
        'doc_title': 'doc_title',
        'custom_stop_words': 'custom_stop_words',
        'summary_length': 'summary_length',
        'context_amount': 'context_amount',
        'short_sentence_length': 'short_sentence_length',
        'long_sentence_length': 'long_sentence_length'
    }

    def __init__(self, dataset=None, doc_title=None, custom_stop_words=None, summary_length=None, context_amount=None, short_sentence_length=None, long_sentence_length=None):  # noqa: E501
        """SummarizeDocs - a model defined in Swagger"""  # noqa: E501

        self._dataset = None
        self._doc_title = None
        self._custom_stop_words = None
        self._summary_length = None
        self._context_amount = None
        self._short_sentence_length = None
        self._long_sentence_length = None
        self.discriminator = None

        self.dataset = dataset
        self.doc_title = doc_title
        if custom_stop_words is not None:
            self.custom_stop_words = custom_stop_words
        if summary_length is not None:
            self.summary_length = summary_length
        if context_amount is not None:
            self.context_amount = context_amount
        if short_sentence_length is not None:
            self.short_sentence_length = short_sentence_length
        if long_sentence_length is not None:
            self.long_sentence_length = long_sentence_length

    @property
    def dataset(self):
        """Gets the dataset of this SummarizeDocs.  # noqa: E501

        Dataset name.  # noqa: E501

        :return: The dataset of this SummarizeDocs.  # noqa: E501
        :rtype: str
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this SummarizeDocs.

        Dataset name.  # noqa: E501

        :param dataset: The dataset of this SummarizeDocs.  # noqa: E501
        :type: str
        """
        if dataset is None:
            raise ValueError("Invalid value for `dataset`, must not be `None`")  # noqa: E501

        self._dataset = dataset

    @property
    def doc_title(self):
        """Gets the doc_title of this SummarizeDocs.  # noqa: E501

        The title of the document to be summarized.  # noqa: E501

        :return: The doc_title of this SummarizeDocs.  # noqa: E501
        :rtype: str
        """
        return self._doc_title

    @doc_title.setter
    def doc_title(self, doc_title):
        """Sets the doc_title of this SummarizeDocs.

        The title of the document to be summarized.  # noqa: E501

        :param doc_title: The doc_title of this SummarizeDocs.  # noqa: E501
        :type: str
        """
        if doc_title is None:
            raise ValueError("Invalid value for `doc_title`, must not be `None`")  # noqa: E501

        self._doc_title = doc_title

    @property
    def custom_stop_words(self):
        """Gets the custom_stop_words of this SummarizeDocs.  # noqa: E501


        :return: The custom_stop_words of this SummarizeDocs.  # noqa: E501
        :rtype: list[str]
        """
        return self._custom_stop_words

    @custom_stop_words.setter
    def custom_stop_words(self, custom_stop_words):
        """Sets the custom_stop_words of this SummarizeDocs.


        :param custom_stop_words: The custom_stop_words of this SummarizeDocs.  # noqa: E501
        :type: list[str]
        """

        self._custom_stop_words = custom_stop_words

    @property
    def summary_length(self):
        """Gets the summary_length of this SummarizeDocs.  # noqa: E501

        The maximum number of bullet points a user wants to see in each topic summary.  # noqa: E501

        :return: The summary_length of this SummarizeDocs.  # noqa: E501
        :rtype: int
        """
        return self._summary_length

    @summary_length.setter
    def summary_length(self, summary_length):
        """Sets the summary_length of this SummarizeDocs.

        The maximum number of bullet points a user wants to see in each topic summary.  # noqa: E501

        :param summary_length: The summary_length of this SummarizeDocs.  # noqa: E501
        :type: int
        """

        self._summary_length = summary_length

    @property
    def context_amount(self):
        """Gets the context_amount of this SummarizeDocs.  # noqa: E501

        The number of sentences surrounding key summary sentences in the documents that they come from.  # noqa: E501

        :return: The context_amount of this SummarizeDocs.  # noqa: E501
        :rtype: int
        """
        return self._context_amount

    @context_amount.setter
    def context_amount(self, context_amount):
        """Sets the context_amount of this SummarizeDocs.

        The number of sentences surrounding key summary sentences in the documents that they come from.  # noqa: E501

        :param context_amount: The context_amount of this SummarizeDocs.  # noqa: E501
        :type: int
        """

        self._context_amount = context_amount

    @property
    def short_sentence_length(self):
        """Gets the short_sentence_length of this SummarizeDocs.  # noqa: E501

        The sentence length (in number of words) below which a sentence is excluded from summarization.  # noqa: E501

        :return: The short_sentence_length of this SummarizeDocs.  # noqa: E501
        :rtype: int
        """
        return self._short_sentence_length

    @short_sentence_length.setter
    def short_sentence_length(self, short_sentence_length):
        """Sets the short_sentence_length of this SummarizeDocs.

        The sentence length (in number of words) below which a sentence is excluded from summarization.  # noqa: E501

        :param short_sentence_length: The short_sentence_length of this SummarizeDocs.  # noqa: E501
        :type: int
        """

        self._short_sentence_length = short_sentence_length

    @property
    def long_sentence_length(self):
        """Gets the long_sentence_length of this SummarizeDocs.  # noqa: E501

        The sentence length (in number of words) beyond which a sentence is excluded from summarization.  # noqa: E501

        :return: The long_sentence_length of this SummarizeDocs.  # noqa: E501
        :rtype: int
        """
        return self._long_sentence_length

    @long_sentence_length.setter
    def long_sentence_length(self, long_sentence_length):
        """Sets the long_sentence_length of this SummarizeDocs.

        The sentence length (in number of words) beyond which a sentence is excluded from summarization.  # noqa: E501

        :param long_sentence_length: The long_sentence_length of this SummarizeDocs.  # noqa: E501
        :type: int
        """

        self._long_sentence_length = long_sentence_length

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
        if issubclass(SummarizeDocs, dict):
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
        if not isinstance(other, SummarizeDocs):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
