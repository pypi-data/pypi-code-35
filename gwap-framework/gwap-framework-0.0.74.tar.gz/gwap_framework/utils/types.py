import decimal
from typing import Dict

from schematics.common import DROP, NOT_NONE, NONEMPTY
from schematics.compat import iteritems
from schematics.exceptions import BaseError, CompoundError, ConversionError
from schematics.types import CompoundType, BaseType, StringType, FloatType, IntType, DecimalType, \
    BooleanType


class DictAnyType(CompoundType):
    """A field for storing a mapping of items, the values of which must conform to the type
    specified by the ``field`` parameter.

    Use it like this::

        ...
        categories = DictType(StringType)

    """

    primitive_type = dict
    native_type = dict

    def __init__(self, **kwargs):
        # type: (...) -> typing.Dict[str, T]

        self.field = self._init_field(AnyType, kwargs)
        self.coerce_key = str
        super(DictAnyType, self).__init__(**kwargs)

    @property
    def model_class(self):
        return self.field.model_class

    def _repr_info(self):
        return self.field.__class__.__name__

    def _convert(self, value, context, safe=False):
        data = {}
        errors = {}
        if isinstance(value, list):
            data_list = []
            for val in value:
                data_list.append(self._convert(val, context, safe))
            data = data_list
        else:
            for k, v in iteritems(value):
                try:
                    data[self.coerce_key(k)] = context.field_converter(self.field, v, context)
                except BaseError as exc:
                    errors[k] = exc

        if errors:
            raise CompoundError(errors)
        return data

    def _export(self, dict_instance, format, context):
        """Loops over each item in the model and applies either the field
        transform or the multitype transform.  Essentially functions the same
        as `transforms.export_loop`.
        """
        data = {}
        _export_level = self.field.get_export_level(context)
        if _export_level == DROP:
            return data
        if isinstance(dict_instance, list):
            data_list = []
            for val in dict_instance:
                data_list.append(self._export(val, format=format, context=context))
            return data_list
        for key, value in iteritems(dict_instance):
            shaped = self.field.export(value, format, context)
            if shaped is None:
                if _export_level <= NOT_NONE:
                    continue
            elif self.field.is_compound and len(shaped) == 0:
                if _export_level <= NONEMPTY:
                    continue
            data[key] = shaped
        return data


class AnyType(BaseType):
    """A Unicode string field."""

    primitive_type = str
    native_type = str

    def __init__(self, **kwargs):
        # type: (...) -> typing.Text
        super(AnyType, self).__init__(**kwargs)

    def to_native(self, value, context=None):
        if isinstance(value, str):
            return StringType().to_native(value, context=context)
        elif isinstance(value, int):
            return IntType().to_native(value, context=context)
        elif isinstance(value, float):
            return FloatType().to_native(value, context=context)
        elif isinstance(value, decimal.Decimal):
            return DecimalType().to_native(value, context=context)
        elif isinstance(value, bool) or value == 'false' or value == 'true':
            return BooleanType().to_native(value, context=context)
        elif isinstance(value, list):
            return value
        elif isinstance(value, Dict):
            return value

        raise ConversionError(f"Error when format {value}")
