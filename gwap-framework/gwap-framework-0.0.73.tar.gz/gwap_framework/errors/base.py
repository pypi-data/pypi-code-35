from typing import Dict


class BaseError(Exception):

    def __init__(self, code=None, message=None, status=None):
        Exception.__init__(self)
        self.code = code
        self.message = message
        self.status = status

    def to_dict(self) -> Dict:
        return {
            'code': self.code,
            'message': self.message,
            'status': self.status
        }
