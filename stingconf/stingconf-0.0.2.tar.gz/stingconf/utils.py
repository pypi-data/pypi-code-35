def str_to_type(s):
    t = __builtins__.get(s, None)
    if isinstance(t, type):
        return t
    else:
        return None


def to_upper_snake(name):
    return name.upper().replace('-', '_')
