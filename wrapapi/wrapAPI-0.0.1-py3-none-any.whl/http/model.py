
from requests import Response, Session

from wrapapi.http.element import (
    find,
    Report,
    ResponseBody,
    ResponseJson,
    ResponseHeaders,
    ResponseUrl,
)


class AppResponse(object):

    def __init__(self, response: Response, report):
        self._response = response
        self._report = report
        self._url = response.url
        self._body = None
        self._json = None
        self._url = None
        self._headers = None

    def __str__(self):
        return f'<Response [{self.status_code}] {self._url}>'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return (
            f'<Response[{self.status_code}]: '
            f'{self.method} {self.url}, '
            f'{self.body}, '
            f'{self.headers}>'
        )

    @property
    def method(self) -> str:
        return self._response.request.method.upper()

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def url(self) -> ResponseUrl:
        if not self._url:
            self._url = ResponseUrl(self._response)
        return self._url

    @property
    def json(self) -> ResponseJson:
        if not self._json:
            self._json = ResponseJson(self._response, self._report)
        return self._json

    @property
    def body(self) -> ResponseBody:
        if not self._body:
            # self._response.request.body()
            self._body = ResponseBody(self._response)
        return self._body

    @property
    def headers(self) -> ResponseHeaders:
        if not self._headers:
            self._headers = ResponseHeaders(self._response)
        return self._headers

    def key(self, path):
        return find(self._json, path)

    # def should_status(self, code: int) -> bool:
    #     msg = f'expected: {code}, current {self.status_code}'
    #     assert bool(self.status_code == code), Report(self, [msg]).build()
    #     return True


class AppRequest(object):

    def __init__(self, config):
        self._session = Session()
        self.config = config
        self.response: AppResponse = None
        self._report = None

    def _request(
        self,
        method,
        url,
        status_code=None,
        params=None,
        data=None,
        headers=None,
        files=None,
        cookies=None,
        json=None,
        auth=None
    ) -> AppResponse:

        res = self._session.request(
            method=method.upper(),
            url=f'{self.config.base_url}{url}' if self.config.base_url else url,
            params=params,
            data=data,
            files=files,
            cookies=cookies or self.config.cookie,
            headers=headers or self.config.headers,
            verify=self.config.verify,
            # hooks=dict(response=self.config.logger),
            timeout=self.config.timeout,
            json=json,
            auth=auth,
        )
        self.response = AppResponse(res, report=self.report)
        if status_code:
            # TODO need implemented report
            assert self.response.status_code == status_code
        return self.response

    def get(self, url, *, params=None, status=None) -> AppResponse:
        res = self._request(
            method='GET',
            url=url,
            status_code=status,
            params=params
        )
        return res

    def post(self, url, *, data=None, status=None) -> AppResponse:
        res = self._request(
            method='POST',
            url=url,
            status_code=status,
            json=data
        )
        return res

    def put(self, url, *, data=None, status=None) -> AppResponse:
        res = self._request(
            method='PUT',
            url=url,
            status_code=status,
            json=data
        )
        return res

    def patch(self, url, *, data=None, status=None) -> AppResponse:
        res = self._request(
            method='PATCH',
            url=url,
            status_code=status,
            json=data
        )
        return res

    def delete(self, url, *, status=None) -> AppResponse:
        res = self._request(
            method='DELETE',
            url=url,
            status_code=status
        )
        return res

    @property
    def report(self) -> Report:
        if not self._report:
            self._report = Report()
        return self._report
