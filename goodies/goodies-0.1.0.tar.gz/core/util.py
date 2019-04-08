def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError as te:
        return False
