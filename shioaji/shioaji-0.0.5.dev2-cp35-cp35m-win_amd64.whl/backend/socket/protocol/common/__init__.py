from shioaji.backend.socket.protocol.common.handler import (
    login_in,
    login_out,
)

tr_map = {
    20000: (login_in, login_out),
}

__all__ = [
    'tr_map',
    'login_in',
    'login_out',
]
