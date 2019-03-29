from datetime import date, datetime
from decimal import Decimal
from jsonschema import validate, FormatChecker
from flask import json
from .exceptions import SerializerError
import uuid

from jsonschema.exceptions import ValidationError


uuid_schema = {
    'type': 'string',
    'pattern': r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'  # noqa
}


alphanumeric_schema = {
    'type': 'string',
    'pattern': '^[a-zA-Z0-9_]*$'
}


class BaseSerializer(object):
    """
    Base serializer
    """
    _schema = {}

    _json = {}

    _json_to_validate = {}

    def __init__(self, payload=None, request=None, data=None):
        """
        A serializer object can be built from a request object or
        a model object
        """

        if 'properties' not in self._schema:
            raise SerializerError(
                'Can not build a serializer without a schema associated')
        else:
            self._properties = self._schema['properties']

        if request:
            self._initialize_from_dict(request.json)

        elif data:
            self._initialize_from_dict(data)

        elif payload:
            data = json.loads(payload, parse_float=Decimal)
            self._initialize_from_dict(data)
        else:
            raise SerializerError(
                'Can not build a serializer without an'
                'http request or data dictionary associated')

    def custom_converter(self, o):
        if type(o) == uuid.UUID:
            return str(o)
        elif type(o) == date:
            return o.isoformat()
        elif type(o) == datetime:
            return o.astimezone().isoformat()

    def _validate(self):
        # avoid extra values not defined in the schema
        if 'additionalProperties' not in self._schema:
            self._schema['additionalProperties'] = False

        try:
            validate(
                self._json_to_validate, self._schema,
                format_checker=FormatChecker())
        except ValidationError as e:
            instances = (
                uuid.UUID, date, datetime
            )
            if type(e.instance) in instances:
                # jsonchema can not deal with uuid validation
                # so string conversion is a way to handle this
                self._json_to_validate = json.loads(
                    self.dumps(), parse_float=Decimal)
            validate(
                self._json_to_validate, self._schema,
                format_checker=FormatChecker())
        finally:
            self._json_to_validate = None

    def _initialize_from_dict(self, data):
        """
        Loads serializer from a request object
        """
        self._json = data
        self._json_to_validate = data.copy()
        self._validate()

    @property
    def json(self):
        """
        Returns a json representation
        """
        return self._json

    @json.setter
    def set_json(self, value):
        raise NotImplementedError

    def dumps(self):
        return json.dumps(self.json, default=self.custom_converter)
