# system modules
import logging
import textwrap
import socket
import io
from http.client import parse_headers, HTTPResponse

# internal modules

# external modules


logger = logging.getLogger(__name__)

# SSDP discovery adapted from
# https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python

SSDP_BROADCAST_ADDR = "239.255.255.250"
SSDP_BROADCAST_PORT = 1900

SSDP_SONY_CAMERA_REMOTE_API_SERVICE = (
    "urn:schemas-sony-com:service:ScalarWebAPI:1"
)


class FakeSocket:
    """
    Fake socket for use with a :any:`http.client.HTTPResponse`

    .. note::

        The idea was adapted from `e-lean.cn
        <https://www.e-learn.cn/content/wangluowenzhang/153473>`_.
    """

    def __init__(self, response_bytes):
        self._file = io.BytesIO(response_bytes)

    def makefile(self, *args, **kwargs):
        return self._file


def discover(service, timeout=2):
    """
    Discover a ``service`` via SSDP

    .. note::

        The method was adapted from `electronicmonk.nl
        <https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python>`_.

    Args:
        service (str): the service to discover
        timeout (float, optional): timeout in seconds. Defaults to ``2``.

    Returns:
        sequence of dict : sequence of discovered service dictionaries with the
        keys ``location``, ``usn``, ``st`` and ``addr`` (tuple of address and
        port of the response).
    """
    request_line = "M-SEARCH * HTTP/1.1"
    request_headers = {
        "HOST": "{}:{}".format(SSDP_BROADCAST_ADDR, SSDP_BROADCAST_PORT),
        "ST": service,
        "MX": timeout,
        "MAN": '"ssdp:discover"',
    }
    request = "\r\n".join(
        (
            request_line,
            "\r\n".join(
                "{}: {}".format(k, v) for k, v in request_headers.items()
            ),
            "\r\n",
        )
    )
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.settimeout(timeout)
    logger.debug("Sending SSDP broadcast:\n{}".format(request))
    s.sendto(request.encode(), (SSDP_BROADCAST_ADDR, SSDP_BROADCAST_PORT))
    services = []
    try:
        while True:
            data, addr = s.recvfrom(65507)
            logger.debug(
                "Got response from {}:\n{}".format(addr, data.decode())
            )
            response = HTTPResponse(FakeSocket(data))
            response.begin()
            headers = {k.lower(): v for k, v in response.getheaders()}
            props = {k: headers.get(k) for k in ("location", "usn", "st")}
            props["addr"] = addr
            services.append(props)
    except socket.timeout:
        pass
    s.close()
    return tuple(services)
