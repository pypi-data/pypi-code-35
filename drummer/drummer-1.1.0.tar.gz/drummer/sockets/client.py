#!/usr/bin/python3
# -*- coding: utf-8 -*-
from drummer.foundation import Response
from .commonsocket import CommonSocket


class SocketClientException(Exception):
    pass


class SocketClient(CommonSocket):

    def __init__(self, config):

        super().__init__(config)


    def send_request(self, request):

        # init socket
        sock = self.sock
        server_address = self.server_address
        MSG_LEN = self.MSG_LEN

        # establish a connection
        try:
            sock.connect(server_address)

        except ConnectionRefusedError as e:
            raise SocketClientException('Socket refused connection')

        except Exception:
            raise SocketClientException('Connection error')

        try:
            # encode and send request
            encoded_request = request.encode(MSG_LEN)

            res = sock.sendall(encoded_request)
            if res:
                raise SocketClientException('Cannot send request message to server')

            # get data from server and decode
            encoded_response = self.receive_data(sock)

            response = Response.decode(encoded_response)

        except:
            raise SocketClientException('Impossible to send request to server')

        finally:
            # close connection
            sock.close()

        return response


    def get_response(self, sock):

        response = b''
        receiving = True
        while receiving:

            new_data = sock.recv(self.MSG_LEN)
            if new_data:
                response += new_data
            else:
                receiving = False

        return response
