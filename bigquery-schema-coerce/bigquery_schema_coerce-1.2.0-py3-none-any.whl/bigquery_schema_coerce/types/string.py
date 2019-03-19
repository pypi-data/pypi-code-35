def convert_string_field(schema_field, candidate_attribute):
    if schema_field.mode == "REPEATED":
        return list(convert_string_repeated(candidate_attribute))
    return convert_string(candidate_attribute)


def convert_string(candidate_attribute):
    return str(candidate_attribute)


def convert_string_repeated(candidate_attribute):
    for attribute_value in candidate_attribute:
        yield convert_string(attribute_value)
