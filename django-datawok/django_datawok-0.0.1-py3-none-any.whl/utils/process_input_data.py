from .get_field_type import get_field_type
from dateutil import parser
from datetime import datetime
from django.shortcuts import get_object_or_404


class Processor:
    @staticmethod
    def process_boolean(datum, field, model):
        if datum.lower() == "false":
            return False
        else:
            return bool(datum)

    @staticmethod
    def process_date(datum, field_name, model):
        if isinstance(datum, datetime):
            return datum
        else:
            return parser.parse(datum)

    @staticmethod
    def process_foreign(datum, field_name, model):
        related_model = [
            field
            for field in model._meta.get_fields()
            if field.name == field_name
        ][0].related_model
        return get_object_or_404(related_model, pk=datum)

    @staticmethod
    def process_string(datum, field_name, model):
        return datum

    @staticmethod
    def process_float(datum, field_name, model):
        return float(datum)

    @staticmethod
    def process_integer(datum, field_name, model):
        return int(datum)


def process_input_data(model, data):
    fields = {}

    for field in model._meta.get_fields():
        field_type = get_field_type(field)
        field_type = field_type if field_type else "unsupported"
        fields[field.name] = field_type

    for row in data:
        for field_name, datum in row.items():
            field_type = fields[field_name]
            process_func = getattr(
                Processor,
                "process_{}".format(field_type),
                lambda datum, field, model: datum,
            )
            row[field_name] = process_func(datum, field_name, model)

    return data
