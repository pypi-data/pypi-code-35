import functools as ft


def trace(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        print(
            'TRACE: Calling {}() with position arguments {} and '
            'keyword arguments {}'.format(
                func.__name__, args, kwargs))
        result = func(*args, **kwargs)
        print(
            'TRACE: {}() returned {}'.format(
                func.__name__, result))
        return result
    return wrapper


class show_status:

    def __init__(self, message):
        self.message = message

    def __call__(self, func):
        
        @ft.wraps(func)
        def wrapper(*args, **kwargs):
            print('{} ... '.format(self.message), end='')
            result = func(*args, **kwargs)
            print('success.')
            return result
        return wrapper
