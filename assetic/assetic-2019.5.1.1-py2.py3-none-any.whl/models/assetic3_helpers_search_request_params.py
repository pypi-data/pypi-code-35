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

##from assetic.models.kendo_mvc_i_filter_descriptor import KendoMvcIFilterDescriptor  # noqa: F401,E501
##from assetic.models.kendo_mvc_sort_descriptor import KendoMvcSortDescriptor  # noqa: F401,E501


class Assetic3HelpersSearchRequestParams(object):
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
        'search_type': 'int',
        'source_tile_id': 'str',
        'sorts': 'list[KendoMvcSortDescriptor]',
        'filters': 'list[KendoMvcIFilterDescriptor]',
        'page': 'int',
        'page_size': 'int'
    }

    attribute_map = {
        'id': 'Id',
        'search_type': 'SearchType',
        'source_tile_id': 'SourceTileId',
        'sorts': 'Sorts',
        'filters': 'Filters',
        'page': 'Page',
        'page_size': 'PageSize'
    }

    def __init__(self, id=None, search_type=None, source_tile_id=None, sorts=None, filters=None, page=None, page_size=None):  # noqa: E501
        """Assetic3HelpersSearchRequestParams - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._search_type = None
        self._source_tile_id = None
        self._sorts = None
        self._filters = None
        self._page = None
        self._page_size = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if search_type is not None:
            self.search_type = search_type
        if source_tile_id is not None:
            self.source_tile_id = source_tile_id
        if sorts is not None:
            self.sorts = sorts
        if filters is not None:
            self.filters = filters
        if page is not None:
            self.page = page
        if page_size is not None:
            self.page_size = page_size

    @property
    def id(self):
        """Gets the id of this Assetic3HelpersSearchRequestParams.  # noqa: E501


        :return: The id of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Assetic3HelpersSearchRequestParams.


        :param id: The id of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def search_type(self):
        """Gets the search_type of this Assetic3HelpersSearchRequestParams.  # noqa: E501


        :return: The search_type of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :rtype: int
        """
        return self._search_type

    @search_type.setter
    def search_type(self, search_type):
        """Sets the search_type of this Assetic3HelpersSearchRequestParams.


        :param search_type: The search_type of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :type: int
        """

        self._search_type = search_type

    @property
    def source_tile_id(self):
        """Gets the source_tile_id of this Assetic3HelpersSearchRequestParams.  # noqa: E501


        :return: The source_tile_id of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :rtype: str
        """
        return self._source_tile_id

    @source_tile_id.setter
    def source_tile_id(self, source_tile_id):
        """Sets the source_tile_id of this Assetic3HelpersSearchRequestParams.


        :param source_tile_id: The source_tile_id of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :type: str
        """

        self._source_tile_id = source_tile_id

    @property
    def sorts(self):
        """Gets the sorts of this Assetic3HelpersSearchRequestParams.  # noqa: E501


        :return: The sorts of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :rtype: list[KendoMvcSortDescriptor]
        """
        return self._sorts

    @sorts.setter
    def sorts(self, sorts):
        """Sets the sorts of this Assetic3HelpersSearchRequestParams.


        :param sorts: The sorts of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :type: list[KendoMvcSortDescriptor]
        """

        self._sorts = sorts

    @property
    def filters(self):
        """Gets the filters of this Assetic3HelpersSearchRequestParams.  # noqa: E501


        :return: The filters of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :rtype: list[KendoMvcIFilterDescriptor]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this Assetic3HelpersSearchRequestParams.


        :param filters: The filters of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :type: list[KendoMvcIFilterDescriptor]
        """

        self._filters = filters

    @property
    def page(self):
        """Gets the page of this Assetic3HelpersSearchRequestParams.  # noqa: E501


        :return: The page of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this Assetic3HelpersSearchRequestParams.


        :param page: The page of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :type: int
        """

        self._page = page

    @property
    def page_size(self):
        """Gets the page_size of this Assetic3HelpersSearchRequestParams.  # noqa: E501


        :return: The page_size of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this Assetic3HelpersSearchRequestParams.


        :param page_size: The page_size of this Assetic3HelpersSearchRequestParams.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

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
        if issubclass(Assetic3HelpersSearchRequestParams, dict):
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
        if not isinstance(other, Assetic3HelpersSearchRequestParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
