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


class Assetic3IntegrationRepresentationsDataExchangeTask(object):
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
        'job_name': 'str',
        'type': 'int',
        'stage': 'int',
        'status': 'int',
        'status_description': 'str',
        'sys_background_worker_id': 'str',
        'request_user': 'str',
        'start_time': 'str',
        'end_time': 'str',
        'summary': 'str',
        'data_exchange_profile': 'str',
        'module': 'int',
        'target_type': 'int',
        'source_type': 'int',
        'source_info': 'str',
        'target_name': 'str',
        'error_document_id': 'str',
        'message': 'str',
        'links': 'list[WebApiHalLink]',
        'embedded': 'list[WebApiHalEmbeddedResource]'
    }

    attribute_map = {
        'id': 'Id',
        'job_name': 'JobName',
        'type': 'Type',
        'stage': 'Stage',
        'status': 'Status',
        'status_description': 'StatusDescription',
        'sys_background_worker_id': 'SysBackgroundWorkerId',
        'request_user': 'RequestUser',
        'start_time': 'StartTime',
        'end_time': 'EndTime',
        'summary': 'Summary',
        'data_exchange_profile': 'DataExchangeProfile',
        'module': 'Module',
        'target_type': 'TargetType',
        'source_type': 'SourceType',
        'source_info': 'SourceInfo',
        'target_name': 'TargetName',
        'error_document_id': 'ErrorDocumentId',
        'message': 'Message',
        'links': '_links',
        'embedded': '_embedded'
    }

    def __init__(self, id=None, job_name=None, type=None, stage=None, status=None, status_description=None, sys_background_worker_id=None, request_user=None, start_time=None, end_time=None, summary=None, data_exchange_profile=None, module=None, target_type=None, source_type=None, source_info=None, target_name=None, error_document_id=None, message=None, links=None, embedded=None):  # noqa: E501
        """Assetic3IntegrationRepresentationsDataExchangeTask - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._job_name = None
        self._type = None
        self._stage = None
        self._status = None
        self._status_description = None
        self._sys_background_worker_id = None
        self._request_user = None
        self._start_time = None
        self._end_time = None
        self._summary = None
        self._data_exchange_profile = None
        self._module = None
        self._target_type = None
        self._source_type = None
        self._source_info = None
        self._target_name = None
        self._error_document_id = None
        self._message = None
        self._links = None
        self._embedded = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if job_name is not None:
            self.job_name = job_name
        if type is not None:
            self.type = type
        if stage is not None:
            self.stage = stage
        if status is not None:
            self.status = status
        if status_description is not None:
            self.status_description = status_description
        if sys_background_worker_id is not None:
            self.sys_background_worker_id = sys_background_worker_id
        if request_user is not None:
            self.request_user = request_user
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if summary is not None:
            self.summary = summary
        if data_exchange_profile is not None:
            self.data_exchange_profile = data_exchange_profile
        if module is not None:
            self.module = module
        if target_type is not None:
            self.target_type = target_type
        if source_type is not None:
            self.source_type = source_type
        if source_info is not None:
            self.source_info = source_info
        if target_name is not None:
            self.target_name = target_name
        if error_document_id is not None:
            self.error_document_id = error_document_id
        if message is not None:
            self.message = message
        if links is not None:
            self.links = links
        if embedded is not None:
            self.embedded = embedded

    @property
    def id(self):
        """Gets the id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param id: The id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def job_name(self):
        """Gets the job_name of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The job_name of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._job_name

    @job_name.setter
    def job_name(self, job_name):
        """Sets the job_name of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param job_name: The job_name of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._job_name = job_name

    @property
    def type(self):
        """Gets the type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: int
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param type: The type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: int
        """

        self._type = type

    @property
    def stage(self):
        """Gets the stage of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The stage of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: int
        """
        return self._stage

    @stage.setter
    def stage(self, stage):
        """Sets the stage of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param stage: The stage of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: int
        """

        self._stage = stage

    @property
    def status(self):
        """Gets the status of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The status of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param status: The status of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: int
        """

        self._status = status

    @property
    def status_description(self):
        """Gets the status_description of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The status_description of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._status_description

    @status_description.setter
    def status_description(self, status_description):
        """Sets the status_description of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param status_description: The status_description of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._status_description = status_description

    @property
    def sys_background_worker_id(self):
        """Gets the sys_background_worker_id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The sys_background_worker_id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._sys_background_worker_id

    @sys_background_worker_id.setter
    def sys_background_worker_id(self, sys_background_worker_id):
        """Sets the sys_background_worker_id of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param sys_background_worker_id: The sys_background_worker_id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._sys_background_worker_id = sys_background_worker_id

    @property
    def request_user(self):
        """Gets the request_user of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The request_user of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._request_user

    @request_user.setter
    def request_user(self, request_user):
        """Sets the request_user of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param request_user: The request_user of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._request_user = request_user

    @property
    def start_time(self):
        """Gets the start_time of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The start_time of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param start_time: The start_time of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The end_time of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param end_time: The end_time of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._end_time = end_time

    @property
    def summary(self):
        """Gets the summary of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The summary of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """Sets the summary of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param summary: The summary of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._summary = summary

    @property
    def data_exchange_profile(self):
        """Gets the data_exchange_profile of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The data_exchange_profile of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._data_exchange_profile

    @data_exchange_profile.setter
    def data_exchange_profile(self, data_exchange_profile):
        """Sets the data_exchange_profile of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param data_exchange_profile: The data_exchange_profile of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._data_exchange_profile = data_exchange_profile

    @property
    def module(self):
        """Gets the module of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The module of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: int
        """
        return self._module

    @module.setter
    def module(self, module):
        """Sets the module of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param module: The module of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: int
        """

        self._module = module

    @property
    def target_type(self):
        """Gets the target_type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The target_type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: int
        """
        return self._target_type

    @target_type.setter
    def target_type(self, target_type):
        """Sets the target_type of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param target_type: The target_type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: int
        """

        self._target_type = target_type

    @property
    def source_type(self):
        """Gets the source_type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The source_type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: int
        """
        return self._source_type

    @source_type.setter
    def source_type(self, source_type):
        """Sets the source_type of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param source_type: The source_type of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: int
        """

        self._source_type = source_type

    @property
    def source_info(self):
        """Gets the source_info of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The source_info of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._source_info

    @source_info.setter
    def source_info(self, source_info):
        """Sets the source_info of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param source_info: The source_info of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._source_info = source_info

    @property
    def target_name(self):
        """Gets the target_name of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The target_name of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._target_name

    @target_name.setter
    def target_name(self, target_name):
        """Sets the target_name of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param target_name: The target_name of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._target_name = target_name

    @property
    def error_document_id(self):
        """Gets the error_document_id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The error_document_id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._error_document_id

    @error_document_id.setter
    def error_document_id(self, error_document_id):
        """Sets the error_document_id of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param error_document_id: The error_document_id of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._error_document_id = error_document_id

    @property
    def message(self):
        """Gets the message of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The message of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param message: The message of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def links(self):
        """Gets the links of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The links of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: list[WebApiHalLink]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param links: The links of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :type: list[WebApiHalLink]
        """

        self._links = links

    @property
    def embedded(self):
        """Gets the embedded of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501


        :return: The embedded of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
        :rtype: list[WebApiHalEmbeddedResource]
        """
        return self._embedded

    @embedded.setter
    def embedded(self, embedded):
        """Sets the embedded of this Assetic3IntegrationRepresentationsDataExchangeTask.


        :param embedded: The embedded of this Assetic3IntegrationRepresentationsDataExchangeTask.  # noqa: E501
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
        if issubclass(Assetic3IntegrationRepresentationsDataExchangeTask, dict):
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
        if not isinstance(other, Assetic3IntegrationRepresentationsDataExchangeTask):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
