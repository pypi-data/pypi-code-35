import re


def convert_int_field(schema_field, candidate_attribute):
    if schema_field.mode == "REPEATED":
        return list(convert_int_repeated(candidate_attribute))
    return convert_int(candidate_attribute)


def convert_int(candidate_attribute):
    if isinstance(candidate_attribute, str):
        candidate_attribute = re.sub("[^0-9.]", "", candidate_attribute)
    return int(candidate_attribute)


def convert_int_repeated(candidate_attribute):
    for attribute_value in candidate_attribute:
        yield convert_int(attribute_value)
