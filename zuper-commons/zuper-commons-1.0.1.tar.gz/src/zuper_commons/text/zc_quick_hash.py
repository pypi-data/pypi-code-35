

__all__ = [
    'get_md5',
    'get_sha1',
]

def get_md5(contents: bytes) -> str:
    """ Returns an hexdigest (string) """
    from zuper_commons.types import check_isinstance
    check_isinstance(contents, bytes)
    import hashlib
    m = hashlib.md5()
    m.update(contents)
    s = m.hexdigest()
    check_isinstance(s, str)
    return s


def get_sha1(contents: bytes) -> str:
    """ Returns an hexdigest (string) """
    from zuper_commons.types import check_isinstance
    import hashlib
    check_isinstance(contents, bytes)
    m = hashlib.sha1()
    m.update(contents)
    s = m.hexdigest()
    check_isinstance(s, str)
    return s
