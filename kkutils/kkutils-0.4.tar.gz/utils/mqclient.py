#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Email: kai.zhang1@nio.com
Last modified: 2018-09-29 00:59:38
'''
import asyncio
import json
import os

import aio_pika
from aio_pika import Message
from utils import JSONEncoder
from utils import Logger


class MQClient:

    def __init__(self, queue='test', workers=50, **kwargs):
        if 'host' in kwargs or 'port' in kwargs:
            host = kwargs.pop('host', 'localhost')
            port = kwargs.pop('port', 5672)
            user = kwargs.pop('user', 'guest')
            pwd = kwargs.pop('pwd', 'guest')
            self.uri = f'amqp://{user}:{pwd}@{host}:{port}'
        elif 'uri' in kwargs:
            self.uri = kwargs.pop('uri')
        else:
            self.uri = os.environ.get('MQ_URI', 'amqp://guest:guest@localhost:5672')
        self.queue_name = queue
        self.routing_key = queue
        self.workers = workers
        self.loop = asyncio.get_event_loop()
        self.logger = Logger()
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.uri, loop=self.loop)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name, auto_delete=False)
        await self.channel.set_qos(prefetch_count=self.workers)
        self.logger.info(f'rabbitmq server connected: {repr(self.channel)}, queue: {self.queue_name}')

    async def consume(self, process):
        # await self.queue.consume(process)
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                await process(message)

    async def publish(self, doc):
        msg = json.dumps(doc, cls=JSONEncoder).encode()
        await self.channel.default_exchange.publish(Message(msg),
                                                    routing_key=self.routing_key)

    async def shutdown(self):
        await self.channel.close()
        await self.connection.close()
