import base64


def _base64_encode_string(value):
    """

    This method is just a wrapper that handle the incompatibility between the
    standard_b64encode() method on versions 2 and 3 of Python. On Python 2, a
    string is returned, but on Python 3, a bytes-class instance is returned.

    """
    value_base64 = base64.standard_b64encode(value)
    if type(value_base64) is str:
        return value_base64
    elif type(value_base64) is bytes or type(value_base64) is bytearray:
        return value_base64.decode('ascii')
