from datetime import datetime


def int_type_test(value):
    if type(value) == str:
        int(value)
    else:
        assert int(value) == value


def float_type_test(value):
    if type(value) == str:
        float(value)
    else:
        assert float(value) == value


def datetime_type_test(value):
    assert type(value) == datetime
