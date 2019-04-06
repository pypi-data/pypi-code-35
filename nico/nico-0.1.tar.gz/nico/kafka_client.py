#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pykafka import KafkaClient


def get_kafka_client(kafka_hosts):
    return KafkaClient(hosts=kafka_hosts)
