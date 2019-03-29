from starlette.routing import Route
from . endpoints import register_v0, confirm_v0

ROUTES = [
    Route('/v0/register', register_v0, name='register_v0', methods=['POST']),
    Route('/v0/confirm/{confirmation_code}', confirm_v0, name='confirm_v0', methods=['GET'])
]