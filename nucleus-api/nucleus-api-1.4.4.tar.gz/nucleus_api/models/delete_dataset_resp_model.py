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


class DeleteDatasetRespModel(object):
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
        'job_id': 'str',
        'result': 'object'
    }

    attribute_map = {
        'job_id': 'job_id',
        'result': 'result'
    }

    def __init__(self, job_id=None, result=None):  # noqa: E501
        """DeleteDatasetRespModel - a model defined in Swagger"""  # noqa: E501

        self._job_id = None
        self._result = None
        self.discriminator = None

        if job_id is not None:
            self.job_id = job_id
        if result is not None:
            self.result = result

    @property
    def job_id(self):
        """Gets the job_id of this DeleteDatasetRespModel.  # noqa: E501

        If the job is taking too long, job_id is returned, GET /jobs can then be used to poll for results  # noqa: E501

        :return: The job_id of this DeleteDatasetRespModel.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this DeleteDatasetRespModel.

        If the job is taking too long, job_id is returned, GET /jobs can then be used to poll for results  # noqa: E501

        :param job_id: The job_id of this DeleteDatasetRespModel.  # noqa: E501
        :type: str
        """

        self._job_id = job_id

    @property
    def result(self):
        """Gets the result of this DeleteDatasetRespModel.  # noqa: E501

        Dataset deleted  # noqa: E501

        :return: The result of this DeleteDatasetRespModel.  # noqa: E501
        :rtype: object
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this DeleteDatasetRespModel.

        Dataset deleted  # noqa: E501

        :param result: The result of this DeleteDatasetRespModel.  # noqa: E501
        :type: object
        """

        self._result = result

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
        if issubclass(DeleteDatasetRespModel, dict):
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
        if not isinstance(other, DeleteDatasetRespModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
