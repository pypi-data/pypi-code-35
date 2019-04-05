from aiohttp import ClientResponse


class BinanceException(Exception):
    pass


class BinanceAPIException(BinanceException):
    def __init__(self, response: ClientResponse, response_json: dict):
        self.api_code = response_json['code']
        self.api_message = response_json['msg']
        self.http_code = response.status

        self.response = response
        self.request_info = response.request_info

    def __str__(self):  # pragma: no cover
        return f'APIError(http_code={self.http_code}, api_code={self.api_code}): {self.api_message}'


class BinanceResponseException(BinanceException):
    pass
