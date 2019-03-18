#!/usr/bin/env python3

import asyncio
import traceback

from grpclib.client import Channel

from gv_services.proto.archivist_pb2 import TrafficDataRequest
from gv_services.proto.broadcaster_pb2 import SubRequest
from gv_services.proto.interface_grpc import InterfaceStub
from gv_services.proto.interface_pb2 import PubRequest
from gv_utils import datetime, enums, protobuf
from gv_utils.asyncio import check_event_loop


METRO_PME = enums.DataTypeId.metropme
TOMTOM_FCD = enums.DataTypeId.tomtomfcd


class RpcClient:
    samplings = {METRO_PME: 1*60, TOMTOM_FCD: 1*60}

    def __init__(self, logger, futures=None, callbacks=None):
        if futures is None:
            futures = []
        if callbacks is None:
            callbacks = {}

        self.logger = logger
        self.futures = futures
        self.callbacks = callbacks
        self.interface = None
        self._channel = None
        self._mainfut = None

    async def async_init(self):
        pass

    def start(self, rpchost, rpcport):
        check_event_loop()  # will create a new event loop if needed (if we are not in the main thread)
        self.logger.info('RPC client is starting.')
        try:
            asyncio.run(self._run(rpchost, rpcport))
        except KeyboardInterrupt:
            pass
        self.logger.info('RPC client has stopped.')

    async def _run(self, rpchost, rpcport):
        try:
            self._channel = Channel(rpchost, rpcport, loop=asyncio.get_event_loop())
            self.interface = InterfaceStub(self._channel)
            try:
                await self.async_init()
                self._mainfut = asyncio.gather(
                    *self.futures,
                    *[self._subscribe(datatype, callback) for datatype, callback in self.callbacks.items()]
                )
                self._mainfut.add_done_callback(self._close)
                self.logger.info('RPC client has started.')
                await self._mainfut
            finally:
                self._cancel()
        except:
            self._close()

    def _close(self, _=None):
        if self._channel is not None:
            self._channel.close()
            self._channel = None

    def _cancel(self):
        if self._mainfut is not None:
            self._mainfut.cancel()
            self._mainfut = None

    async def _subscribe(self, datatype, callback):
        async with self.interface.subscribe.open() as stream:
            await stream.send_message(SubRequest(datatype=datatype))
            self.logger.info('RPC client has subscribed to {} data.'.format(datatype))
            try:
                async for response in stream:
                    self.logger.debug('Got new {} data.'.format(datatype))
                    try:
                        trafficdata = await protobuf.decode_traffic_data(response)
                    except:
                        self.logger.error(traceback.format_exc())
                        self.logger.error('An error occurred while decoding {} data to dict.'
                                                      .format(datatype))
                    else:
                        await callback(trafficdata)
            finally:
                await stream.end()
                self.logger.info('RPC client has unsubscribed from {} data.'.format(datatype))

    async def _publish(self, trafficdata, datatype, datatimestamp):
        try:
            async with self.interface.publish.open() as stream:
                request = PubRequest(trafficdata=await protobuf.encode_traffic_data(trafficdata), datatype=datatype)
                request.timestamp.FromSeconds(datatimestamp)
                await stream.send_message(request, end=True)
                response = await stream.recv_message()
                if not response.success:
                    self.logger.warning('Failed to publish {} data.'.format(datatype))
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while publishing {} data.'.format(datatype))

    # TODO: move this to the web app
    async def get_data(self, datatype, datadate):
        try:
            async with self.interface.get_data.open() as stream:
                request = TrafficDataRequest(datatype=datatype)
                request.timestamp.FromSeconds(int(datadate.timestamp()))
                await stream.send_message(request, end=True)
                response = await stream.recv_message()
                self.logger.debug('Got {} data.'.format(datatype))
                try:
                    trafficdata = await protobuf.decode_traffic_data(response)
                except:
                    self.logger.error(traceback.format_exc())
                    self.logger.error('An error occurred while decoding {} data to dict.'.format(datatype))
                else:
                    return trafficdata
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while getting {} data for {}.'
                                          .format(datatype, datetime.to_string(datadate)))


def start(Application, threaded=False):
    if threaded:
        import threading
        threading.Thread(target=start, args=(Application, False), daemon=True).start()
        print('Starting application in a background thread...')
    else:
        Application()
