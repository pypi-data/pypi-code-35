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

from flywheel.models.data_view_analysis_filter_spec import DataViewAnalysisFilterSpec  # noqa: F401,E501
from flywheel.models.data_view_column_spec import DataViewColumnSpec  # noqa: F401,E501
from flywheel.models.data_view_name_filter_spec import DataViewNameFilterSpec  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class DataViewFileSpec(object):

    swagger_types = {
        'container': 'str',
        'analysis_filter': 'DataViewAnalysisFilterSpec',
        'filter': 'DataViewNameFilterSpec',
        'zip_member': 'DataViewNameFilterSpec',
        'match': 'str',
        'format': 'str',
        'format_options': 'object',
        'process_files': 'bool',
        'columns': 'list[DataViewColumnSpec]'
    }

    attribute_map = {
        'container': 'container',
        'analysis_filter': 'analysisFilter',
        'filter': 'filter',
        'zip_member': 'zipMember',
        'match': 'match',
        'format': 'format',
        'format_options': 'formatOptions',
        'process_files': 'processFiles',
        'columns': 'columns'
    }

    rattribute_map = {
        'container': 'container',
        'analysisFilter': 'analysis_filter',
        'filter': 'filter',
        'zipMember': 'zip_member',
        'match': 'match',
        'format': 'format',
        'formatOptions': 'format_options',
        'processFiles': 'process_files',
        'columns': 'columns'
    }

    def __init__(self, container=None, analysis_filter=None, filter=None, zip_member=None, match=None, format=None, format_options=None, process_files=None, columns=None):  # noqa: E501
        """DataViewFileSpec - a model defined in Swagger"""
        super(DataViewFileSpec, self).__init__()

        self._container = None
        self._analysis_filter = None
        self._filter = None
        self._zip_member = None
        self._match = None
        self._format = None
        self._format_options = None
        self._process_files = None
        self._columns = None
        self.discriminator = None
        self.alt_discriminator = None

        self.container = container
        if analysis_filter is not None:
            self.analysis_filter = analysis_filter
        self.filter = filter
        if zip_member is not None:
            self.zip_member = zip_member
        if match is not None:
            self.match = match
        if format is not None:
            self.format = format
        if format_options is not None:
            self.format_options = format_options
        if process_files is not None:
            self.process_files = process_files
        if columns is not None:
            self.columns = columns

    @property
    def container(self):
        """Gets the container of this DataViewFileSpec.

        The type of container (e.g. session)

        :return: The container of this DataViewFileSpec.
        :rtype: str
        """
        return self._container

    @container.setter
    def container(self, container):
        """Sets the container of this DataViewFileSpec.

        The type of container (e.g. session)

        :param container: The container of this DataViewFileSpec.  # noqa: E501
        :type: str
        """

        self._container = container

    @property
    def analysis_filter(self):
        """Gets the analysis_filter of this DataViewFileSpec.


        :return: The analysis_filter of this DataViewFileSpec.
        :rtype: DataViewAnalysisFilterSpec
        """
        return self._analysis_filter

    @analysis_filter.setter
    def analysis_filter(self, analysis_filter):
        """Sets the analysis_filter of this DataViewFileSpec.


        :param analysis_filter: The analysis_filter of this DataViewFileSpec.  # noqa: E501
        :type: DataViewAnalysisFilterSpec
        """

        self._analysis_filter = analysis_filter

    @property
    def filter(self):
        """Gets the filter of this DataViewFileSpec.


        :return: The filter of this DataViewFileSpec.
        :rtype: DataViewNameFilterSpec
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """Sets the filter of this DataViewFileSpec.


        :param filter: The filter of this DataViewFileSpec.  # noqa: E501
        :type: DataViewNameFilterSpec
        """

        self._filter = filter

    @property
    def zip_member(self):
        """Gets the zip_member of this DataViewFileSpec.


        :return: The zip_member of this DataViewFileSpec.
        :rtype: DataViewNameFilterSpec
        """
        return self._zip_member

    @zip_member.setter
    def zip_member(self, zip_member):
        """Sets the zip_member of this DataViewFileSpec.


        :param zip_member: The zip_member of this DataViewFileSpec.  # noqa: E501
        :type: DataViewNameFilterSpec
        """

        self._zip_member = zip_member

    @property
    def match(self):
        """Gets the match of this DataViewFileSpec.

        If multiple file matches are encountered, which file to choose. Default is first

        :return: The match of this DataViewFileSpec.
        :rtype: str
        """
        return self._match

    @match.setter
    def match(self, match):
        """Sets the match of this DataViewFileSpec.

        If multiple file matches are encountered, which file to choose. Default is first

        :param match: The match of this DataViewFileSpec.  # noqa: E501
        :type: str
        """

        self._match = match

    @property
    def format(self):
        """Gets the format of this DataViewFileSpec.

        The expected data file format, default is auto-detect

        :return: The format of this DataViewFileSpec.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """Sets the format of this DataViewFileSpec.

        The expected data file format, default is auto-detect

        :param format: The format of this DataViewFileSpec.  # noqa: E501
        :type: str
        """

        self._format = format

    @property
    def format_options(self):
        """Gets the format_options of this DataViewFileSpec.


        :return: The format_options of this DataViewFileSpec.
        :rtype: object
        """
        return self._format_options

    @format_options.setter
    def format_options(self, format_options):
        """Sets the format_options of this DataViewFileSpec.


        :param format_options: The format_options of this DataViewFileSpec.  # noqa: E501
        :type: object
        """

        self._format_options = format_options

    @property
    def process_files(self):
        """Gets the process_files of this DataViewFileSpec.

        Set to false to skip file reading, and return file attributes instead

        :return: The process_files of this DataViewFileSpec.
        :rtype: bool
        """
        return self._process_files

    @process_files.setter
    def process_files(self, process_files):
        """Sets the process_files of this DataViewFileSpec.

        Set to false to skip file reading, and return file attributes instead

        :param process_files: The process_files of this DataViewFileSpec.  # noqa: E501
        :type: bool
        """

        self._process_files = process_files

    @property
    def columns(self):
        """Gets the columns of this DataViewFileSpec.


        :return: The columns of this DataViewFileSpec.
        :rtype: list[DataViewColumnSpec]
        """
        return self._columns

    @columns.setter
    def columns(self, columns):
        """Sets the columns of this DataViewFileSpec.


        :param columns: The columns of this DataViewFileSpec.  # noqa: E501
        :type: list[DataViewColumnSpec]
        """

        self._columns = columns


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
        if not isinstance(other, DataViewFileSpec):
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
