#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json

from nico.register import register
from nico.kafka_client import get_kafka_client


def message_parser(message):
    try:
        message = json.loads(message)
        message_type = message['type']
        data = message['data']
        created = message['created']
        return message_type, data, created
    except Exception as e:
        logging.error('message parse error', exc_info=True)
        return None


class Consumer(object):

    def __init__(self, topic, consumer_group, settings):
        self.topic = topic
        self.consumer_group = consumer_group
        self.settings = settings
        self.client = get_kafka_client(self.settings['kafka_hosts'])

    def get_consumer(self):
        # from examples.messages import test_message1, test_message2
        # kafka_consumer = [
        #     json.dumps(test_message1()),
        #     json.dumps(test_message2()),
        # ]
        t = self.client.topics[self.topic]
        kafka_consumer = t.get_balanced_consumer(consumer_group=self.consumer_group, managed=True)
        return kafka_consumer

    def run(self):
        consumer = self.get_consumer()
        for message in consumer:
            parser = message_parser(message)
            if parser:
                message_type, data, created = message_parser(message)
                jobs = register.get_jobs(self.topic, message_type)
                for job in jobs:
                    try:
                        job(data)
                        logging.info('job {} run success, topic={}, message_type={}'
                                     .format(job.__name__, self.topic, message_type))
                    except Exception as e:
                        # TODO: retry 三次
                        logging.error('job {} run error'.format(job.__name__), exc_info=True)
