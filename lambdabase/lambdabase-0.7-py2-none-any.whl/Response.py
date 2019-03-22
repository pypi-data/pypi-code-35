import simplejson as json
from abc import ABCMeta, abstractmethod


class Response(object):
    """
    The base response class. All lambda response should inherit from this class.
    It is assumed that the lambdas are using Lambda proxy integration with API
    Gateway and as such need the specific response format from the build() method.
    """
    __metaclass__ = ABCMeta

    _data = {}
    _body = {}
    _code = 200

    def __init__(self, data):
        self._data = data

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def data(self):
        return self._data

    @abstractmethod
    def build(self):
        """
        Return the results as json wrapped in an appropriate format
        """
        return {
            "statusCode": self.code,
            "body": json.dumps(self.body),
            'headers': {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            }
        }


class NoContent(Response):

    def __init__(self):
        super(NoContent, self).__init__({})
        self.code = 204

    def build(self):
        return super(NoContent, self).build()
