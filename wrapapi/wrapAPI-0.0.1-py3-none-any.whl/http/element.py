
from collections import defaultdict

from wrapapi.validations.conditions import Should


def find(content: dict, path: str):
    """
    :param dict content:
    :param str path: item.id
    for example:
        container = {'item': {'id': 123, 'name': 'test'}}
        result = find(container, 'item.id')
        result == 123
    """
    result = None
    for item in path.split('.'):
        result = content[item]
    return result


class ResponseBase(object):

    def __init__(self, request, report):
        self._request = request
        self._report = report
        self._should = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        raise NotImplementedError

    @property
    def should(self) -> Should:
        raise NotImplementedError


class ResponseBody(ResponseBase):
    # TODO must be implemented

    def __str__(self):
        return f'Body: {self._request.request.body}'


class ResponseHeaders(ResponseBase):
    # TODO must be implemented

    def __str__(self):
        return f'Headers: {self._request.headers}'


class ResponseJson(ResponseBase):

    def __str__(self):
        return f'Json: {self._request.json}'

    @property
    def should(self) -> Should:
        if not self._should:
            self._should = Should(self._request, report=self._report)
        return self._should


class ResponseUrl(ResponseBase):

    @property
    def should(self) -> Should:
        # TODO must be implemented
        if not self._should:
            self._should = Should(self._request, report=self._report)
        return self._should

    def __str__(self):
        return f'{self._request.request.method.upper()}: {self._request.url}'


def prepare_response(response) -> str:
    msg = (
        f"\n"
        f"==========================================================="
        f"\n{response.request.method}: {response.url}\n"
        f"-----------------------------------------------------------"
        f"\n\tStatus: {response.status_code}\n"
        f"\tBody: {response.request.body}\n"
        f"\tHeaders: {response.headers}\n"
        f"==========================================================="
        f"\n"
    )
    return msg


def prepare_errors(errors) -> str:
    msg = '\n\t'.join(errors)
    return msg


class Report(object):

    def __init__(self):
        self._errors = defaultdict(list)

    def refresh(self):
        self._errors = defaultdict(list)
        return self._errors

    def add_error(self, response, error):
        self._errors[prepare_response(response)].append(error)
        return self._errors

    def add_if_has_error(self, response, error):
        if error:
            self.add_error(response, error)
        return self._errors

    def build(self) -> str:
        errors = ''
        for response_data, response_errors in self._errors.items():
            errors += response_data + '\n'.join(response_errors)

        self.refresh()
        if errors:
            raise AssertionError(errors)
        return errors
