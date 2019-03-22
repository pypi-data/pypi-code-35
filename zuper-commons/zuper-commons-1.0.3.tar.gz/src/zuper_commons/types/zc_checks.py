from zuper_commons.text import pretty_msg

__all__ = [
    'check_isinstance',
]


def check_isinstance(ob, expected, **kwargs):
    if not isinstance(ob, expected):
        kwargs['object'] = ob
        raise_type_mismatch(ob, expected, **kwargs)


def raise_type_mismatch(ob, expected, **kwargs):
    """ Raises an exception concerning ob having the wrong type. """
    e = 'Object not of expected type:'
    e += '\n  expected: {}'.format(expected)
    e += '\n  obtained: {}'.format(type(ob))
    msg = pretty_msg(e, **kwargs)
    raise ValueError(msg)
