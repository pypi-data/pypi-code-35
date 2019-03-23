# -*- coding: utf-8 -*-

__all__ = [
    'Peer'
]

# std imports
import re
import os
import json
import socket
import base64
import traceback
import threading

# third party
import termcolor

# package imports
from .handler import PeerHandler
from .imports import socketserver, ConnectionRefusedError

# package imports
import net


# globals
SINGLETON = None


# noinspection PyMissingConstructor
class _Peer(socketserver.ThreadingMixIn, socketserver.TCPServer, object):
    # adding to inheritance object for 2.7 support

    # utilities
    ID_REGEX = re.compile(r"(?P<host>.+):(?P<port>\d+) -> (?P<group>.+)")

    # store
    CONNECTIONS = {}
    SUBSCRIPTIONS = {}
    FLAGS = {}

    @staticmethod
    def decode(byte_string):
        """
        Decode a byte string sent from a peer.

        :param byte_string: base64
        :return: str
        """
        try:
            byte_string = base64.b64decode(byte_string).decode('ascii')
            byte_string = json.loads(byte_string)
        except (Exception, json.JSONDecodeError) as err:
            net.LOGGER.debug(byte_string)
            net.LOGGER.debug(err)
            net.LOGGER.debug(traceback.format_exc())

        # if the connection returns data that is not prepackaged as a JSON object, return
        # the raw response as it originally was returned.
        if isinstance(byte_string, dict) and 'raw' in byte_string:
            return byte_string['raw']

        return byte_string

    @classmethod
    def encode(cls, obj):
        """
        Encode an object for delivery.

        :param obj: JSON compatible types
        :return: str
        """
        if not isinstance(obj, dict):
            try:
                if obj in cls.FLAGS:
                    return obj
            except TypeError:
                pass
            obj = {'raw': obj}

        # tag with the peer
        return base64.b64encode(json.dumps(obj).encode('ascii'))

    @staticmethod
    def ports():
        """
        Generator; All ports defined in the environment.

        :return: int
        """
        return [port for port in range(net.PORT_START, net.PORT_START + net.PORT_RANGE)]

    @staticmethod
    def ping(port, host=socket.gethostname()):
        """
        Ping a port and check if it is alive or open.

        :param port: required port to hit
        :param host: host address default is 'localhost'
        :return: bool
        """

        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interface.settimeout(0.25)
        try:
            interface.connect((host, port))
            return True
        except ConnectionRefusedError:
            return False

    @staticmethod
    def generate_id(port, host, group=None):
        """
        Generate a peers id.

        :param port: int
        :param host: str
        :param group: str
        :return: base64
        """

        return base64.b64encode(
            '{host}:{port} -> {group}'.format(
                host=socket.gethostname() if not host else host,
                port=port,
                group=str(group),
            ).encode('ascii')
        )

    # noinspection PyShadowingBuiltins
    @classmethod
    def decode_id(cls, id):
        """
        Decode a peer id

        :param id: base64
        :return: dict {'group': str, 'host': str, 'port': int }
        """
        expr = cls.ID_REGEX.match(base64.b64decode(id).decode('ascii')).groupdict()

        return {
            'group': expr['group'],
            'host': expr['host'],
            'port': int(expr['port'])
        }

    @classmethod
    def build_connection_name(cls, connection):
        """
        Build a connections full name based on the module/name of the function.
        This is then encoded in base64 for easier delivery between peers.

        :param connection: connection
        :return: base64
        """
        return base64.b64encode(
            '{0}.{1}'.format(
                connection.__module__,
                connection.__name__
            ).encode('ascii')
        )

    @classmethod
    def register_connection(cls, connection, tag=None):
        """
        Registers a connection with the global handler.
        Do not use this directly. Instead use the net.connect decorator.

        :func:`net.connect`

        :param tag: str
        :param connection: function
        :return: str
        """
        if not tag:
            tag = cls.build_connection_name(connection)
        else:
            tag = cls.encode(tag)

        # add the connection to the connection registry.
        if tag in cls.CONNECTIONS:
            net.LOGGER.warning(
                "Redefining a connection handler. Be aware, this could cause "
                "unexpected results."
            )
        cls.CONNECTIONS[tag] = connection

        return tag

    @classmethod
    def register_subscriber(cls, event, peer, connection):
        """
        Registers the peer and connection to the peers subscription system. This
        is for internal use only, use the ``net.subscribe`` decorator instead.

        :param event: event id
        :param peer: peer id
        :param connection: connection id
        :return: None
        """
        subscription = cls.SUBSCRIPTIONS.setdefault(event, {})
        peer_connection = subscription.setdefault(peer, [])
        peer_connection.append(connection)

    @classmethod
    def register_flag(cls, flag, handler):
        """
        Registers a flag with the peer server. Flags are simple responses that
        can trigger error handling or logging. Do not use this directly. Instead
        use the net.flag decorator.

        @net.flag("SOME_ERROR")
        def your_next_function(peer, connection):
            raise SomeError(
                "This failed because {0} failed on the other peer.".format(
                    connection
                )
            )

        :param flag: payload
        :param handler: function
        :return: base64
        """

        flag = base64.b64encode(flag.encode('ascii'))

        if flag in cls.FLAGS:
            net.LOGGER.warning(
                "Redefining a flag handler. Be aware, this could cause "
                "unexpected results."
            )

        cls.FLAGS[flag] = handler

        return flag

    @classmethod
    def process_flags(cls, response):
        """
        Check a response and test if it should be processed as a flag.

        :param response: Anything
        :return: response from the registered process
        """
        # handle flags
        try:
            if response in cls.FLAGS:
                return cls.FLAGS[response]
        except TypeError:
            pass

    @classmethod
    def get_flag(cls, flag):
        """
        Get a flags id.

        :param flag: str
        :return: str
        """
        encoded = base64.b64encode(flag.encode('ascii'))

        # validate the flag requested
        if encoded not in cls.FLAGS:
            raise Exception("Invalid Flag requested.")

        return encoded

    def __init__(self, launch=True, test=False, group=None):

        # mask with singleton catch unless being tested
        if SINGLETON and not test:
            raise RuntimeError(
                "Can not create a new peer in without shutting down the previous"
                " one. Please use net.Peer() instead."
            )

        # find port
        self._host = net.HOST_IP
        self._port = self.scan_for_port()
        self._group = net.GROUP if not group else group
        self._is_hub = net.IS_HUB

        # handle threading
        self._thread = threading.Thread(target=self.serve_forever)
        self._thread.daemon = True

        # launch the peer
        if launch:
            self.launch()

    @property
    def hub(self):
        """
        Defines if this peer acts as the hub for communication through the
        network.

        :return: bool
        """
        return self._is_hub

    @property
    def group(self):
        """
        Group this peer is assigned to.

        :return: str
        """
        return self._group

    @property
    def port(self):
        """
        Port that the peer is running on.

        :return: int
        """
        return self._port

    @property
    def host(self):
        """
        Host that the peer is running on.

        :return: str
        """
        return self._host

    @property
    def id(self):
        """
        Get this peers id. This is tethered to the port and the executable path
        the peer was launched with. This is base64 encoded for easier delivery.

        :return: base64
        """
        return self.generate_id(self.port, self.host, self.group)

    @property
    def friendly_id(self, peer_id=None):
        """
        Get the peers id in a friendly displayable way.

        :return: str
        """
        if not peer_id:
            peer_id = self.id

        # decode and hand back
        friendly = self.decode_id(peer_id)
        friendly['hub'] = self._is_hub
        return friendly

    def scan_for_port(self):
        """
        Scan for a free port to bind to. You can override the default port range and search range by setting the
        environment variables NET_PORT NET_PORT_RANGE.

        Port range:
            default 3010-3050

        :return: int
        """
        # cast as int and default to 3010 and 40
        port = net.PORT_START
        port_range = port + net.PORT_RANGE

        net.LOGGER.debug("Scanning {0} ports for open port...".format(port_range - port))
        while port <= port_range:

            # ping the local host ports
            if not self.ping(port):
                try:
                    super(_Peer, self).__init__((self.host, port), PeerHandler)
                    net.LOGGER.debug("Found Port: {0}".format(termcolor.colored(port, "green")))
                    break
                except (OSError, ConnectionRefusedError):
                    net.LOGGER.warning("Stale Port: {0}".format(termcolor.colored(port, "yellow")))

            port += 1

        # throw error if there is no open port
        if port > port_range:
            raise ValueError("No open port found between {0} - {1}".format(port, port_range))

        # return found port
        return port

    def launch(self):
        """
        Launch the peer. This should only be used if Peer(launch=False).
        Otherwise this is executed at init.

        """
        self._thread.start()

    def request(self, peer, connection, args, kwargs):
        """
        Request an action and response from a peer.

        :param peer: base64 encoded peer id
        :param connection: the target connection id to run
        :param args: positional arguments to pass to the target connection (must be json compatible)
        :param kwargs: keyword arguments to pass to the target connection (must be json compatible)
        :return: response from peer
        """
        # decode
        if not isinstance(peer, tuple):
            expr = self.decode_id(peer)
            peer = (expr['host'], expr['port'])

        # package up the request, by default delete the peer argument in the kwargs.
        if kwargs.get("peer"):
            del kwargs['peer']
        payload = {'connection': connection.decode('ascii'), 'args': args, 'kwargs': kwargs}

        # socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set the time out on the function
        if kwargs.get('time_out'):
            sock.settimeout(kwargs.get('time_out'))

        # connect
        sock.connect(peer)

        try:
            # send request
            sock.sendall(self.encode(payload))

            # sock
            raw = sock.recv(1024)

            # safely close the socket
            sock.close()

        except Exception as err:
            # safely close the socket
            sock.close()

            # handle error logging
            net.LOGGER.error(traceback.format_exc())
            raise err

        # handle flags
        processor = self.process_flags(raw)
        if processor:
            terminate = processor(
                connection,
                {
                    'host': peer[0],
                    'port': peer[1],
                }
            )

            # if flag returns anything, return it
            if terminate:
                return terminate

        # decode and return final response
        return self.decode(raw)

    def trigger_event(self, event, *args, **kwargs):
        """
        Registers the peer and connection to the peers subscription system. This
        is for internal use only, use the ``net.subscribe`` decorator instead.

        :param event: event id
        :param args: args to pass to the subscribed connections
        :param kwargs: args to pass to the subscribed connections
        :return: None
        """
        event = self.SUBSCRIPTIONS.get(event)

        if not event:
            raise Exception(
                "Invalid Event. Registered Events:\n" + '\n'.join(
                    sorted(self.SUBSCRIPTIONS.keys())
                )
            )

        # loop over the peers
        for peer, connections in event.items():
            for connection in connections:
                self.request(peer, connection, args, kwargs)


# noinspection PyPep8Naming
def Peer(*args, **kwargs):
    """
    Running Peer server for this instance of python.

    :return: :class:`net.peer._Peer`
    """
    global SINGLETON

    # handle singleton behavior
    if not SINGLETON:
        SINGLETON = _Peer(*args, **kwargs)

    return SINGLETON