def pipeline(X, steps, settings=None):
    if settings is None:
        settings = {}

    res = [X]
    for name, func in steps:
        res = func(*res, **step_settings(name, settings))

    return res


def step_settings(step_name, settings):
    step_name_prefix = f'{step_name}_'
    result = {}

    for key, value in settings.items():
        if key.startswith(step_name_prefix):
            param_name = key.replace(step_name_prefix, '', 1)
            result[param_name] = value

    return result
