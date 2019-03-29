from functools import wraps


def coerce():
    def coerce_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            for kwarg, ktype in func.__annotations__.items():
                if kwarg == "return":
                    continue
                if kwarg in kwargs:
                    try:
                        kwargs[kwarg] = ktype(kwargs[kwarg])
                    except Exception:
                        print("ERROR, coercing")
            result = func(*args, **kwargs)
            return result

        return func_wrapper

    return coerce_decorator
