from dateutil.parser import parse as parse_date


def convert_timestamp_field(schema_field, candidate_attribute):
    if schema_field.mode == "REPEATED":
        return list(convert_timestamp_repeated(candidate_attribute))
    return convert_timestamp(candidate_attribute)


def convert_timestamp(candidate_attribute):
    return parse_date(candidate_attribute).isoformat()


def convert_timestamp_repeated(candidate_attribute):
    for attribute_value in candidate_attribute:
        yield convert_timestamp(attribute_value)
