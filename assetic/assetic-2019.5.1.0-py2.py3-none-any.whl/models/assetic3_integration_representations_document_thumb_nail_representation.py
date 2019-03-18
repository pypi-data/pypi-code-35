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


class Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation(object):
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
        'mime_type': 'str',
        'main_data_stream': 'str',
        'data_stream': 'str',
        'name': 'str',
        'label': 'str',
        'id': 'str',
        'group_name': 'str',
        'category_name': 'str',
        'sub_category_name': 'str',
        'full_path': 'str',
        'thumb_nail_path': 'str',
        'is_image': 'bool',
        'links': 'list[WebApiHalLink]',
        'embedded': 'list[WebApiHalEmbeddedResource]'
    }

    attribute_map = {
        'mime_type': 'MimeType',
        'main_data_stream': 'MainDataStream',
        'data_stream': 'DataStream',
        'name': 'Name',
        'label': 'Label',
        'id': 'Id',
        'group_name': 'GroupName',
        'category_name': 'CategoryName',
        'sub_category_name': 'SubCategoryName',
        'full_path': 'FullPath',
        'thumb_nail_path': 'ThumbNailPath',
        'is_image': 'IsImage',
        'links': '_links',
        'embedded': '_embedded'
    }

    def __init__(self, mime_type=None, main_data_stream=None, data_stream=None, name=None, label=None, id=None, group_name=None, category_name=None, sub_category_name=None, full_path=None, thumb_nail_path=None, is_image=None, links=None, embedded=None):  # noqa: E501
        """Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation - a model defined in Swagger"""  # noqa: E501

        self._mime_type = None
        self._main_data_stream = None
        self._data_stream = None
        self._name = None
        self._label = None
        self._id = None
        self._group_name = None
        self._category_name = None
        self._sub_category_name = None
        self._full_path = None
        self._thumb_nail_path = None
        self._is_image = None
        self._links = None
        self._embedded = None
        self.discriminator = None

        if mime_type is not None:
            self.mime_type = mime_type
        if main_data_stream is not None:
            self.main_data_stream = main_data_stream
        if data_stream is not None:
            self.data_stream = data_stream
        if name is not None:
            self.name = name
        if label is not None:
            self.label = label
        if id is not None:
            self.id = id
        if group_name is not None:
            self.group_name = group_name
        if category_name is not None:
            self.category_name = category_name
        if sub_category_name is not None:
            self.sub_category_name = sub_category_name
        if full_path is not None:
            self.full_path = full_path
        if thumb_nail_path is not None:
            self.thumb_nail_path = thumb_nail_path
        if is_image is not None:
            self.is_image = is_image
        if links is not None:
            self.links = links
        if embedded is not None:
            self.embedded = embedded

    @property
    def mime_type(self):
        """Gets the mime_type of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The mime_type of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type):
        """Sets the mime_type of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param mime_type: The mime_type of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._mime_type = mime_type

    @property
    def main_data_stream(self):
        """Gets the main_data_stream of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The main_data_stream of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._main_data_stream

    @main_data_stream.setter
    def main_data_stream(self, main_data_stream):
        """Sets the main_data_stream of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param main_data_stream: The main_data_stream of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._main_data_stream = main_data_stream

    @property
    def data_stream(self):
        """Gets the data_stream of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The data_stream of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._data_stream

    @data_stream.setter
    def data_stream(self, data_stream):
        """Sets the data_stream of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param data_stream: The data_stream of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._data_stream = data_stream

    @property
    def name(self):
        """Gets the name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param name: The name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def label(self):
        """Gets the label of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The label of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param label: The label of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def id(self):
        """Gets the id of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The id of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param id: The id of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def group_name(self):
        """Gets the group_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The group_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        """Sets the group_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param group_name: The group_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._group_name = group_name

    @property
    def category_name(self):
        """Gets the category_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The category_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._category_name

    @category_name.setter
    def category_name(self, category_name):
        """Sets the category_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param category_name: The category_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._category_name = category_name

    @property
    def sub_category_name(self):
        """Gets the sub_category_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The sub_category_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._sub_category_name

    @sub_category_name.setter
    def sub_category_name(self, sub_category_name):
        """Sets the sub_category_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param sub_category_name: The sub_category_name of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._sub_category_name = sub_category_name

    @property
    def full_path(self):
        """Gets the full_path of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The full_path of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._full_path

    @full_path.setter
    def full_path(self, full_path):
        """Sets the full_path of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param full_path: The full_path of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._full_path = full_path

    @property
    def thumb_nail_path(self):
        """Gets the thumb_nail_path of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The thumb_nail_path of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: str
        """
        return self._thumb_nail_path

    @thumb_nail_path.setter
    def thumb_nail_path(self, thumb_nail_path):
        """Sets the thumb_nail_path of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param thumb_nail_path: The thumb_nail_path of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: str
        """

        self._thumb_nail_path = thumb_nail_path

    @property
    def is_image(self):
        """Gets the is_image of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The is_image of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: bool
        """
        return self._is_image

    @is_image.setter
    def is_image(self, is_image):
        """Sets the is_image of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param is_image: The is_image of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: bool
        """

        self._is_image = is_image

    @property
    def links(self):
        """Gets the links of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The links of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: list[WebApiHalLink]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param links: The links of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :type: list[WebApiHalLink]
        """

        self._links = links

    @property
    def embedded(self):
        """Gets the embedded of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501


        :return: The embedded of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
        :rtype: list[WebApiHalEmbeddedResource]
        """
        return self._embedded

    @embedded.setter
    def embedded(self, embedded):
        """Sets the embedded of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.


        :param embedded: The embedded of this Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation.  # noqa: E501
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
        if issubclass(Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation, dict):
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
        if not isinstance(other, Assetic3IntegrationRepresentationsDocumentThumbNailRepresentation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
