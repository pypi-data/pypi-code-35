import re


def convert_float_field(schema_field, candidate_attribute):
    if schema_field.mode == "REPEATED":
        return list(convert_float_repeated(candidate_attribute))
    return convert_float(candidate_attribute)


def convert_float(candidate_attribute):
    if isinstance(candidate_attribute, str):
        candidate_attribute = re.sub("[^0-9.]", "", candidate_attribute)
    return float(candidate_attribute)


def convert_float_repeated(candidate_attribute):
    for attribute_value in candidate_attribute:
        yield convert_float(attribute_value)
