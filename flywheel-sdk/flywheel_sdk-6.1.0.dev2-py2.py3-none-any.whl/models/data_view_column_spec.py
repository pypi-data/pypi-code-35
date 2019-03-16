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


class DataViewColumnSpec(object):

    swagger_types = {
        'src': 'str',
        'dst': 'str',
        'type': 'str',
        'expr': 'str'
    }

    attribute_map = {
        'src': 'src',
        'dst': 'dst',
        'type': 'type',
        'expr': 'expr'
    }

    rattribute_map = {
        'src': 'src',
        'dst': 'dst',
        'type': 'type',
        'expr': 'expr'
    }

    def __init__(self, src=None, dst=None, type=None, expr=None):  # noqa: E501
        """DataViewColumnSpec - a model defined in Swagger"""
        super(DataViewColumnSpec, self).__init__()

        self._src = None
        self._dst = None
        self._type = None
        self._expr = None
        self.discriminator = None
        self.alt_discriminator = None

        self.src = src
        if dst is not None:
            self.dst = dst
        if type is not None:
            self.type = type
        if expr is not None:
            self.expr = expr

    @property
    def src(self):
        """Gets the src of this DataViewColumnSpec.

        The source property in the format of {container}.{field}

        :return: The src of this DataViewColumnSpec.
        :rtype: str
        """
        return self._src

    @src.setter
    def src(self, src):
        """Sets the src of this DataViewColumnSpec.

        The source property in the format of {container}.{field}

        :param src: The src of this DataViewColumnSpec.  # noqa: E501
        :type: str
        """

        self._src = src

    @property
    def dst(self):
        """Gets the dst of this DataViewColumnSpec.

        The optional destination property name

        :return: The dst of this DataViewColumnSpec.
        :rtype: str
        """
        return self._dst

    @dst.setter
    def dst(self, dst):
        """Sets the dst of this DataViewColumnSpec.

        The optional destination property name

        :param dst: The dst of this DataViewColumnSpec.  # noqa: E501
        :type: str
        """

        self._dst = dst

    @property
    def type(self):
        """Gets the type of this DataViewColumnSpec.

        The type that this value should be translated to (for typed output)

        :return: The type of this DataViewColumnSpec.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DataViewColumnSpec.

        The type that this value should be translated to (for typed output)

        :param type: The type of this DataViewColumnSpec.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def expr(self):
        """Gets the expr of this DataViewColumnSpec.

        An optional expression, allowing simple calculations (add, subtract, multiply, divide). Use 'x' to substitute the column

        :return: The expr of this DataViewColumnSpec.
        :rtype: str
        """
        return self._expr

    @expr.setter
    def expr(self, expr):
        """Sets the expr of this DataViewColumnSpec.

        An optional expression, allowing simple calculations (add, subtract, multiply, divide). Use 'x' to substitute the column

        :param expr: The expr of this DataViewColumnSpec.  # noqa: E501
        :type: str
        """

        self._expr = expr


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
        if not isinstance(other, DataViewColumnSpec):
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
