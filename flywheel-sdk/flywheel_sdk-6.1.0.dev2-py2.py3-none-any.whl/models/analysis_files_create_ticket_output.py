# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 6.1.0-dev.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class AnalysisFilesCreateTicketOutput(object):

    swagger_types = {
        'ticket': 'str',
        'filename': 'str',
        'file_cnt': 'int',
        'size': 'int'
    }

    attribute_map = {
        'ticket': 'ticket',
        'filename': 'filename',
        'file_cnt': 'file_cnt',
        'size': 'size'
    }

    rattribute_map = {
        'ticket': 'ticket',
        'filename': 'filename',
        'file_cnt': 'file_cnt',
        'size': 'size'
    }

    def __init__(self, ticket=None, filename=None, file_cnt=None, size=None):  # noqa: E501
        """AnalysisFilesCreateTicketOutput - a model defined in Swagger"""
        super(AnalysisFilesCreateTicketOutput, self).__init__()

        self._ticket = None
        self._filename = None
        self._file_cnt = None
        self._size = None
        self.discriminator = None
        self.alt_discriminator = None

        self.ticket = ticket
        self.filename = filename
        self.file_cnt = file_cnt
        self.size = size

    @property
    def ticket(self):
        """Gets the ticket of this AnalysisFilesCreateTicketOutput.


        :return: The ticket of this AnalysisFilesCreateTicketOutput.
        :rtype: str
        """
        return self._ticket

    @ticket.setter
    def ticket(self, ticket):
        """Sets the ticket of this AnalysisFilesCreateTicketOutput.


        :param ticket: The ticket of this AnalysisFilesCreateTicketOutput.  # noqa: E501
        :type: str
        """

        self._ticket = ticket

    @property
    def filename(self):
        """Gets the filename of this AnalysisFilesCreateTicketOutput.


        :return: The filename of this AnalysisFilesCreateTicketOutput.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this AnalysisFilesCreateTicketOutput.


        :param filename: The filename of this AnalysisFilesCreateTicketOutput.  # noqa: E501
        :type: str
        """

        self._filename = filename

    @property
    def file_cnt(self):
        """Gets the file_cnt of this AnalysisFilesCreateTicketOutput.


        :return: The file_cnt of this AnalysisFilesCreateTicketOutput.
        :rtype: int
        """
        return self._file_cnt

    @file_cnt.setter
    def file_cnt(self, file_cnt):
        """Sets the file_cnt of this AnalysisFilesCreateTicketOutput.


        :param file_cnt: The file_cnt of this AnalysisFilesCreateTicketOutput.  # noqa: E501
        :type: int
        """

        self._file_cnt = file_cnt

    @property
    def size(self):
        """Gets the size of this AnalysisFilesCreateTicketOutput.


        :return: The size of this AnalysisFilesCreateTicketOutput.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this AnalysisFilesCreateTicketOutput.


        :param size: The size of this AnalysisFilesCreateTicketOutput.  # noqa: E501
        :type: int
        """

        self._size = size


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AnalysisFilesCreateTicketOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
