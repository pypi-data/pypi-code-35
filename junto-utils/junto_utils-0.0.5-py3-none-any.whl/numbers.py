def get_int_value(value, default=None):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return default
    else:
        return value
