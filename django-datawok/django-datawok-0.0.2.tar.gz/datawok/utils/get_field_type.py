from datawok.constants import (
    STRING_FIELDS,
    DATE_FIELDS,
    BOOLEAN_FIELDS,
    FK_FIELDS,
    INTEGER_FIELDS,
    FLOAT_FIELDS,
)


def get_field_type(field):
    for field_type in STRING_FIELDS:
        if isinstance(field, field_type):
            return "string"

    for field_type in DATE_FIELDS:
        if isinstance(field, field_type):
            return "date"

    for field_type in BOOLEAN_FIELDS:
        if isinstance(field, field_type):
            return "boolean"

    for field_type in INTEGER_FIELDS:
        if isinstance(field, field_type):
            return "integer"

    for field_type in FLOAT_FIELDS:
        if isinstance(field, field_type):
            return "float"

    for field_type in FK_FIELDS:
        if isinstance(field, field_type):
            return "foreign"

    return None
