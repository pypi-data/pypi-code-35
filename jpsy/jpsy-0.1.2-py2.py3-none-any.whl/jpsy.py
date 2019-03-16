from functools import partial


def pythonified_key(key):
    if not isinstance(key, str) or key.isupper():
        return key
    is_prev_upper = False
    chars = []
    for i, char in enumerate(key):
        lower = char.lower()
        is_upper = char.isupper()
        if is_upper and i and not is_prev_upper:
            chars.append("_{}".format(lower))
        else:
            chars.append(lower)
        is_prev_upper = is_upper
    return "".join(chars)


def jsified_key(key):
    if not isinstance(key, str) or key.isupper():
        return key
    tokens = key.split("_")
    return "".join([tokens[0]] + [t.title() for t in tokens[1:]])


def converter(dict_obj, key_converter):
    result = {}
    for key, value in dict_obj.items():
        converted_key = key_converter(key)
        if isinstance(value, dict):
            converted_value = converter(value, key_converter)
        else:
            converted_value = value
        result[converted_key] = converted_value
    return result


pythonify = partial(converter, key_converter=pythonified_key)
jsify = partial(converter, key_converter=jsified_key)
