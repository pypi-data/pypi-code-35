"""
GoodWan client library: serializer
"""
import logging

from goodwan_client.devices import DEVICES_BY_ID
from goodwan_client.errors import ParseError
from goodwan_client.helpers import str_to_datetime

logger = logging.getLogger("goodwan")


class Serializer:
    def __init__(self, timezone):
        """
        Constructor
        :param timezone: pytz timezone
        :type timezone: pytz.timezone
        """
        self.timezone = timezone

    def objectify(self, data, cls):
        """
        Deserialize data
        :param data: data to objectify
        :type data: dict
        :param cls: class
        :type cls: type
        :return: object of type cls
        """
        if not isinstance(data, dict):
            raise ParseError("Data item is not a dict")

        obj = cls()
        for field, field_parser in cls.__dict__.items():
            if not field.startswith("__"):
                if issubclass(field_parser, ObjectifyField):
                    if field not in data:
                        raise ParseError("No \"{}\" field in data item"
                                         .format(field))
                    val = field_parser.parse_data(data[field], self)
                elif issubclass(field_parser, GeneratedField):
                    val = field_parser.generate(data, self)
                elif hasattr(field_parser, "__call__"):
                    if field not in data:
                        raise ParseError("No \"{}\" field in data item"
                                         .format(field))
                    try:
                        val = field_parser(data[field])
                    except Exception as err:
                        raise ValueError("Cannot parse field \"{}\": {}"
                                         .format(field, err))
                else:
                    raise ValueError("Wrong field \"{}\" parser for class {}"
                                     .format(field, cls.__class__.__name__))
                setattr(obj, field, val)

        return obj


class ObjectifyField:
    """ Basic field class for objectify'able field data """
    @staticmethod
    def parse_data(data, serializer):
        raise NotImplementedError("Cannot use ObjectifyField class itself")


class GeneratedField:
    """  Basic field class for generated field data """
    @staticmethod
    def generate(all_data, serializer):
        raise NotImplementedError("Cannot use GeneratedField class itself")


class DateTimeField(ObjectifyField):
    """ Datetime field for objectify'able class """
    @staticmethod
    def parse_data(data, serializer):
        """
        Parse data
        :param data: data
        :type data: str
        :param serializer: serializer
        :type serializer: Serializer
        """
        return str_to_datetime(data, serializer.timezone)


class DeviceGenerator(GeneratedField):
    @staticmethod
    def generate(all_data, serializer):
        """
        Generate device
        :param all_data: all data
        :type all_data: dict
        :param serializer: serializer
        :type serializer: Serializer
        :return: device object
        :rtype: Device
        """
        for k in ("data_type", "data", "data_ext"):
            if k not in all_data:
                logging.warning("Got packet without data_type")
                return None

        device_id = all_data["data_type"]

        if device_id in DEVICES_BY_ID:
            cls = DEVICES_BY_ID[device_id]
            try:
                return cls(all_data)
            except (ValueError, TypeError) as err:
                logging.exception("Error parsing data for device {}: {}"
                                  .format(cls.name, err))
                return None
        else:
            logging.warning("Unsupported device id {}".format(device_id))
            return None


class DeviceNameGenerator(GeneratedField):
    @staticmethod
    def generate(all_data, serializer):
        """
        Generate device
        :param all_data: all data
        :type all_data: dict
        :param serializer: serializer
        :type serializer: Serializer
        :return: device object
        :rtype: Device
        """
        if "data_type" in all_data and all_data["data_type"] in DEVICES_BY_ID:
            return DEVICES_BY_ID[all_data["data_type"]].name
        else:
            return None
