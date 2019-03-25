# -*- coding: utf-8 -*-
"""
Handler Module
--------------

Contains the peer handler and should have nothing else.
"""

__all__ = [
    'PeerHandler',
]

# std imports
import traceback

# package imports
import net

# python 2/3 imports
from .imports import socketserver


class PeerHandler(socketserver.BaseRequestHandler):
    """
    Handles all incoming requests to the applications Peer server.
    Do not modify or interact with directly.
    """

    # noinspection PyPep8Naming
    def handle(self):
        """
        Handles all incoming requests to the server.
        """
        raw = self.request.recv(1024)

        # response codes
        null = self.server.get_flag('NULL')
        invalid_connection = self.server.get_flag('INVALID_CONNECTION')

        # if there is no data, bail and don't respond
        if not raw:
            self.request.sendall(null)
            return

        # convert from json
        try:
            data = self.server.decode(raw)

            # skip if there is no data in the request
            if not data:
                self.request.sendall(null)
                return

            # pull in the connection registered on this peer. The name passed
            # could be a string.
            connection = None

            # TODO: This needs to be addressed in the future. Would prefer to
            #  get away from the byte encoding. The following for loop logic can
            #  be removed once this is figured out.
            names = [data['connection'], data['connection'].encode('ascii')]
            for name in names:
                connection = self.server.CONNECTIONS.get(name)
                if connection:
                    break

            # throw invalid if the connection doesn't exist on this peer.
            if not connection:
                self.request.sendall(invalid_connection)
                return

            # execute the connection handler and send back
            response = self.server.encode(connection(*data['args'], **data['kwargs']))
            self.request.sendall(response)

        except Exception as err:
            net.LOGGER.error(err)
            net.LOGGER.error(traceback.format_exc())
            packet = {
                'payload': 'error',
                'traceback': traceback.format_exc()
            }
            payload = self.server.encode(packet)
            self.request.sendall(payload)
