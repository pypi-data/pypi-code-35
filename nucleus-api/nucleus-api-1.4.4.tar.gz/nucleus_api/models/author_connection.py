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


class AuthorConnection(object):
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
        'target_author': 'str',
        'query': 'str',
        'custom_stop_words': 'list[str]',
        'metadata_selection': 'object',
        'time_period': 'str',
        'period_start': 'str',
        'period_end': 'str',
        'excluded_docs': 'list[str]'
    }

    attribute_map = {
        'dataset': 'dataset',
        'target_author': 'target_author',
        'query': 'query',
        'custom_stop_words': 'custom_stop_words',
        'metadata_selection': 'metadata_selection',
        'time_period': 'time_period',
        'period_start': 'period_start',
        'period_end': 'period_end',
        'excluded_docs': 'excluded_docs'
    }

    def __init__(self, dataset=None, target_author=None, query=None, custom_stop_words=None, metadata_selection=None, time_period=None, period_start=None, period_end=None, excluded_docs=None):  # noqa: E501
        """AuthorConnection - a model defined in Swagger"""  # noqa: E501

        self._dataset = None
        self._target_author = None
        self._query = None
        self._custom_stop_words = None
        self._metadata_selection = None
        self._time_period = None
        self._period_start = None
        self._period_end = None
        self._excluded_docs = None
        self.discriminator = None

        self.dataset = dataset
        self.target_author = target_author
        if query is not None:
            self.query = query
        if custom_stop_words is not None:
            self.custom_stop_words = custom_stop_words
        if metadata_selection is not None:
            self.metadata_selection = metadata_selection
        if time_period is not None:
            self.time_period = time_period
        if period_start is not None:
            self.period_start = period_start
        if period_end is not None:
            self.period_end = period_end
        if excluded_docs is not None:
            self.excluded_docs = excluded_docs

    @property
    def dataset(self):
        """Gets the dataset of this AuthorConnection.  # noqa: E501

        Dataset name.  # noqa: E501

        :return: The dataset of this AuthorConnection.  # noqa: E501
        :rtype: str
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this AuthorConnection.

        Dataset name.  # noqa: E501

        :param dataset: The dataset of this AuthorConnection.  # noqa: E501
        :type: str
        """
        if dataset is None:
            raise ValueError("Invalid value for `dataset`, must not be `None`")  # noqa: E501

        self._dataset = dataset

    @property
    def target_author(self):
        """Gets the target_author of this AuthorConnection.  # noqa: E501

        Name of the author to be analyzed.  # noqa: E501

        :return: The target_author of this AuthorConnection.  # noqa: E501
        :rtype: str
        """
        return self._target_author

    @target_author.setter
    def target_author(self, target_author):
        """Sets the target_author of this AuthorConnection.

        Name of the author to be analyzed.  # noqa: E501

        :param target_author: The target_author of this AuthorConnection.  # noqa: E501
        :type: str
        """
        if target_author is None:
            raise ValueError("Invalid value for `target_author`, must not be `None`")  # noqa: E501

        self._target_author = target_author

    @property
    def query(self):
        """Gets the query of this AuthorConnection.  # noqa: E501

        Fulltext query, using mysql MATCH boolean query format. Example, (\"word1\" OR \"word2\") AND (\"word3\" OR \"word4\")  # noqa: E501

        :return: The query of this AuthorConnection.  # noqa: E501
        :rtype: str
        """
        return self._query

    @query.setter
    def query(self, query):
        """Sets the query of this AuthorConnection.

        Fulltext query, using mysql MATCH boolean query format. Example, (\"word1\" OR \"word2\") AND (\"word3\" OR \"word4\")  # noqa: E501

        :param query: The query of this AuthorConnection.  # noqa: E501
        :type: str
        """

        self._query = query

    @property
    def custom_stop_words(self):
        """Gets the custom_stop_words of this AuthorConnection.  # noqa: E501


        :return: The custom_stop_words of this AuthorConnection.  # noqa: E501
        :rtype: list[str]
        """
        return self._custom_stop_words

    @custom_stop_words.setter
    def custom_stop_words(self, custom_stop_words):
        """Sets the custom_stop_words of this AuthorConnection.


        :param custom_stop_words: The custom_stop_words of this AuthorConnection.  # noqa: E501
        :type: list[str]
        """

        self._custom_stop_words = custom_stop_words

    @property
    def metadata_selection(self):
        """Gets the metadata_selection of this AuthorConnection.  # noqa: E501

        JSON object specifying metadata-based queries on the dataset, of type {\"metadata_field\": \"selected_values\"}  # noqa: E501

        :return: The metadata_selection of this AuthorConnection.  # noqa: E501
        :rtype: object
        """
        return self._metadata_selection

    @metadata_selection.setter
    def metadata_selection(self, metadata_selection):
        """Sets the metadata_selection of this AuthorConnection.

        JSON object specifying metadata-based queries on the dataset, of type {\"metadata_field\": \"selected_values\"}  # noqa: E501

        :param metadata_selection: The metadata_selection of this AuthorConnection.  # noqa: E501
        :type: object
        """

        self._metadata_selection = metadata_selection

    @property
    def time_period(self):
        """Gets the time_period of this AuthorConnection.  # noqa: E501

        Alternative 1: Time period selection  # noqa: E501

        :return: The time_period of this AuthorConnection.  # noqa: E501
        :rtype: str
        """
        return self._time_period

    @time_period.setter
    def time_period(self, time_period):
        """Sets the time_period of this AuthorConnection.

        Alternative 1: Time period selection  # noqa: E501

        :param time_period: The time_period of this AuthorConnection.  # noqa: E501
        :type: str
        """

        self._time_period = time_period

    @property
    def period_start(self):
        """Gets the period_start of this AuthorConnection.  # noqa: E501

        Alternative 2: Start date for the period to analyze within the dataset. Format: \"YYYY-MM-DD HH:MM:SS\"   # noqa: E501

        :return: The period_start of this AuthorConnection.  # noqa: E501
        :rtype: str
        """
        return self._period_start

    @period_start.setter
    def period_start(self, period_start):
        """Sets the period_start of this AuthorConnection.

        Alternative 2: Start date for the period to analyze within the dataset. Format: \"YYYY-MM-DD HH:MM:SS\"   # noqa: E501

        :param period_start: The period_start of this AuthorConnection.  # noqa: E501
        :type: str
        """

        self._period_start = period_start

    @property
    def period_end(self):
        """Gets the period_end of this AuthorConnection.  # noqa: E501

        Alternative 2: End date for the period to analyze within the dataset. Format: \"YYYY-MM-DD HH:MM:SS\"   # noqa: E501

        :return: The period_end of this AuthorConnection.  # noqa: E501
        :rtype: str
        """
        return self._period_end

    @period_end.setter
    def period_end(self, period_end):
        """Sets the period_end of this AuthorConnection.

        Alternative 2: End date for the period to analyze within the dataset. Format: \"YYYY-MM-DD HH:MM:SS\"   # noqa: E501

        :param period_end: The period_end of this AuthorConnection.  # noqa: E501
        :type: str
        """

        self._period_end = period_end

    @property
    def excluded_docs(self):
        """Gets the excluded_docs of this AuthorConnection.  # noqa: E501


        :return: The excluded_docs of this AuthorConnection.  # noqa: E501
        :rtype: list[str]
        """
        return self._excluded_docs

    @excluded_docs.setter
    def excluded_docs(self, excluded_docs):
        """Sets the excluded_docs of this AuthorConnection.


        :param excluded_docs: The excluded_docs of this AuthorConnection.  # noqa: E501
        :type: list[str]
        """

        self._excluded_docs = excluded_docs

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
        if issubclass(AuthorConnection, dict):
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
        if not isinstance(other, AuthorConnection):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
