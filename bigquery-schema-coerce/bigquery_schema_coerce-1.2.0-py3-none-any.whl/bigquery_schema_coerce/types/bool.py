from distutils.util import strtobool


def convert_bool_field(schema_field, candidate_attribute):
    if schema_field.mode == "REPEATED":
        return list(convert_bool_repeated(candidate_attribute))
    return convert_bool(candidate_attribute)


def convert_bool(candidate_attribute):
    if isinstance(candidate_attribute, str):
        candidate_attribute = strtobool(candidate_attribute)
    return bool(candidate_attribute)


def convert_bool_repeated(candidate_attribute):
    for attribute_value in candidate_attribute:
        yield convert_bool(attribute_value)
