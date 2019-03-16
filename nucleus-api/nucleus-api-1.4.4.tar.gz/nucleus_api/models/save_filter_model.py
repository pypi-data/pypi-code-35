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

from nucleus_api.models.filter_model import FilterModel  # noqa: F401,E501


class SaveFilterModel(object):
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
        'filter': 'FilterModel'
    }

    attribute_map = {
        'dataset': 'dataset',
        'filter': 'filter'
    }

    def __init__(self, dataset=None, filter=None):  # noqa: E501
        """SaveFilterModel - a model defined in Swagger"""  # noqa: E501

        self._dataset = None
        self._filter = None
        self.discriminator = None

        self.dataset = dataset
        if filter is not None:
            self.filter = filter

    @property
    def dataset(self):
        """Gets the dataset of this SaveFilterModel.  # noqa: E501

        Dataset name.  # noqa: E501

        :return: The dataset of this SaveFilterModel.  # noqa: E501
        :rtype: str
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this SaveFilterModel.

        Dataset name.  # noqa: E501

        :param dataset: The dataset of this SaveFilterModel.  # noqa: E501
        :type: str
        """
        if dataset is None:
            raise ValueError("Invalid value for `dataset`, must not be `None`")  # noqa: E501

        self._dataset = dataset

    @property
    def filter(self):
        """Gets the filter of this SaveFilterModel.  # noqa: E501


        :return: The filter of this SaveFilterModel.  # noqa: E501
        :rtype: FilterModel
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """Sets the filter of this SaveFilterModel.


        :param filter: The filter of this SaveFilterModel.  # noqa: E501
        :type: FilterModel
        """

        self._filter = filter

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
        if issubclass(SaveFilterModel, dict):
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
        if not isinstance(other, SaveFilterModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
