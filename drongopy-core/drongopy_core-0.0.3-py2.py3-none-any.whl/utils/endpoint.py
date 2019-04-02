import logging
import sys
import traceback

from drongo.status_codes import HttpStatusCodes

__all__ = ['APIEndpoint', 'Endpoint']


class EndpointBase(object):
    __url__ = '/'
    __http_methods__ = ['GET']

    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.valid = True
        self.errors = {}
        self.status = HttpStatusCodes.HTTP_200

    @classmethod
    def do(cls, ctx, **kwargs):
        ep = cls(ctx, **kwargs)
        return ep()

    def call(self):
        raise NotImplementedError

    def set_status(self, status=HttpStatusCodes.HTTP_200):
        self.status = status


class APIEndpoint(EndpointBase):
    _logger = logging.getLogger('api_endpoint')

    def __call__(self):
        self.valid = True
        try:
            self.init()
            self.valid = self.validate()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()

            self._logger.error('\n'.join(traceback.format_exception(
                exc_type, exc_value, exc_traceback)))

            self.error(message='Internal server error.')
            self.ctx.response.set_json({
                'status': 'ERROR',
                'errors': self.errors
            }, status=HttpStatusCodes.HTTP_500)
            return

        if self.valid:
            try:
                self.ctx.response.set_json({
                    'status': 'OK',
                    'payload': self.call()
                }, status=self.status)
                return

            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()

                self._logger.error('\n'.join(traceback.format_exception(
                    exc_type, exc_value, exc_traceback)))

                self.error(message='Internal server error.')
                self.ctx.response.set_json({
                    'status': 'ERROR',
                    'errors': self.errors
                }, status=HttpStatusCodes.HTTP_500)
                return

        self.ctx.response.set_json({
            'status': 'ERROR',
            'errors': self.errors
        }, status=HttpStatusCodes.HTTP_400)

    def error(self, group='_', message=''):
        self.errors.setdefault(group, []).append(message)

    def init(self):
        pass

    def validate(self):
        return True


class Endpoint(EndpointBase):
    _logger = logging.getLogger('endpoint')

    def __call__(self):
        return self.call()
