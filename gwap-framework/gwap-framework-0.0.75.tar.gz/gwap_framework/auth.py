from typing import Union

import jwt
from flask import request, Blueprint

from gwap_framework.app import GwapApp
from gwap_framework.asyncio import get_loop
from gwap_framework.errors.not_authorized import NotAuthorizedError


class GwapAuth:
    """
        GwapAuth is a middleware which guarantees every requests to endpoints are authenticated.
    """
    app = None
    logger = None
    public_key = None

    def __init__(self, app: Union[GwapApp, Blueprint], logger, public_key):
        if not public_key:
            raise Exception('Public key is required.')
        if app:
            self.init_app(app, logger, public_key)

    def init_app(self, app, logger, public_key) -> None:
        """
        :param app: GwapApp
        :param logger: Logger
        :param public_key: a public key
        :return: None
        """
        self.app = app
        self.logger = logger
        self.public_key = public_key

        async def decode_token(token):
            try:
                return jwt.decode(token, self.public_key, algorithms='RS256')
            except Exception as e:
                self.logger.error(f'Error when try decode token: {str(e)}')
                return None

        def authenticate():
            if 'Authorization' in request.headers:
                bearer_token = request.headers.get("Authorization", default=None)
                if bearer_token:
                    payload = get_loop().run_until_complete(decode_token(bearer_token.split("Bearer ")[1]))

                    if payload:
                        request.owner = payload
                        return
            raise NotAuthorizedError()

        if isinstance(app, GwapApp):
            app.before_request_funcs.setdefault(None, []).append(authenticate)
        elif isinstance(app, Blueprint):
            app.before_request(authenticate)
