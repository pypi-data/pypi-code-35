from dappy.exceptions import JSONNotSupportedException


def default_formatter(response):
    return response


def json_formatter(response):
    try:
        return response.json()
    except Exception as e:
        raise JSONNotSupportedException(response)