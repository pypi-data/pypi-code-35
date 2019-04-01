"""An async/await-native http/1.1 client

This is thin glue between the excellent h11 parser/state machine, and trio.

"""

from contextlib import asynccontextmanager
import ssl
from typing import *

import h11
import trio

from mhtg import model


async def tls_connect(server_hostname: AnyStr,
                      tcp_port: int) -> trio.abc.Stream:
    tcp_stream = await trio.open_tcp_stream(server_hostname, tcp_port)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = True
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_stream = trio.SSLStream(transport_stream=tcp_stream,
                                ssl_context=ssl_context,
                                server_hostname=server_hostname,
                                https_compatible=True)

    await ssl_stream.do_handshake()

    return ssl_stream


async def send_file(stream: trio.abc.Stream,
                    obj: model.FilePlaceholder):
    chunk_size = 64 * 1024

    async with await obj.factory() as async_file:
        while True:
            chunk = await async_file.read(chunk_size)
            if not chunk:
                break
            await stream.send_all(chunk)


async def send_data(stream: trio.abc.Stream,
                    obj: Any):
    if obj is None:
        # the event was a ConnectionClosed
        await stream.aclose()
    elif isinstance(obj, (bytes, bytearray, memoryview)):
        await stream.send_all(obj)
    elif isinstance(obj, model.FilePlaceholder):
        await send_file(stream, obj)
    else:
        raise AssertionError(type(obj))


async def send_events(connection: h11.Connection,
                      stream: trio.abc.Stream,
                      *http_events: model.HTTPEvent) -> None:

    for event in http_events:
        data = connection.send_with_data_passthrough(event)
        for obj in data:
            await send_data(stream, obj)


async def receive_events(connection: h11.Connection,
                         stream: trio.abc.Stream) -> AsyncGenerator[model.HTTPEvent, None]:
    while True:
        event = connection.next_event()
        if event is h11.NEED_DATA:
            data = await stream.receive_some(4096)
            connection.receive_data(data)
        else:
            yield event

        if type(event) is h11.EndOfMessage:
            break


def data_collector(data_factory: MutableSequence=bytearray) -> Callable[[Sequence], Any]:
    data = data_factory()
    def collect(chunk=None):
        if chunk is not None:
            data.extend(chunk)
        return data
    return collect


@asynccontextmanager
async def client_factory(server_hostname, port):
    connection = h11.Connection(our_role=h11.CLIENT)
    stream = await tls_connect(server_hostname, port)

    async def make_request(request, data):
        await send_events(connection, stream,
                          request,
                          data,
                          h11.EndOfMessage())

        collect = data_collector()
        response = None

        async for event in receive_events(connection, stream):
            if type(event) is h11.Response:
                response = event
            elif type(event) is h11.Data:
                collect(event.data)
            elif type(event) is h11.EndOfMessage:
                pass
            else:
                raise NotImplementedError(type(event))

        connection.start_next_cycle()

        data = collect()
        return response, data

    try:
        yield make_request
    finally:
        await stream.aclose()
