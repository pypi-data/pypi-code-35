from memory_profiler import profile


def memory_profile(activate=False):
    def wrap(org_func):
        if activate:
            @profile
            def wrapped_func(*args, **kwargs):
                return org_func(*args, **kwargs)
            return wrapped_func
        else:
            def wrapped_func(*args, **kwargs):
                return org_func(*args, **kwargs)
            return wrapped_func

    return wrap
