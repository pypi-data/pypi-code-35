from kafka import KafkaConsumer
import requests
import json
import logging
from splunk_hec_handler import SplunkHecHandler

class KafkaSplunkConnector():
    '''
      :param splunk_data:
          type - dict
          {'host':<splunk host>, 'token':<splunk hec token>, 'port':<port>(default is 8088), 'proto':'http'/'https', 'ssl_verify':True/False}

      :param kafka_data:
          type - dict
	  {'topic':<kafka topic>, 'brokers': list of brokers (type - list), 'auto_offset_rest':<reset value eg. earliest> default is 'earliest', 'auto_commit':True/False}
    '''
    def __init__(self, splunk_data={}, kafka_data={}):
        #Splunk data
        self.splunk_host = splunk_data['host'] if 'host' in splunk_data.keys() else 'localhost'
        self.splunk_token = splunk_data['token'] if 'token' in splunk_data.keys() else ''
        self.splunk_port = splunk_data['port'] if 'port' in splunk_data.keys() else 8088
        self.splunk_proto = splunk_data['proto'] if 'proto' in splunk_data.keys() else 'http'
        self.splunk_source = splunk_data['source'] if 'source' in splunk_data.keys() else ''
        self.splunk_ssl_verify = splunk_data['ssl_verify'] if 'ssl_verify' in splunk_data.keys() else False

        #Kafka data
        self.kafka_topic = kafka_data['topic']
        self.kafka_brokers = kafka_data['brokers']
        self.kafka_auto_offset_reset = kafka_data['auto_offset_reset'] if 'auto_offset_reset' in kafka_data.keys() else 'earliest'
        self.kafka_enable_autocommit = kafka_data['auto_commit'] if 'auto_commit' in kafka_data.keys() else True

    def stream_to_splunk(self):
        logger = logging.getLogger(self.splunk_source)
        logger.setLevel(logging.INFO)
        splunk_handler = SplunkHecHandler(self.splunk_host, self.splunk_token, port=self.splunk_port, proto=self.splunk_proto, ssl_verify = self.splunk_ssl_verify, source=self.splunk_source)
        logger.addHandler(splunk_handler)
        consumer = KafkaConsumer(self.kafka_topic, bootstrap_servers = self.kafka_brokers, auto_offset_reset = self.kafka_auto_offset_reset, enable_auto_commit = self.kafka_enable_autocommit)
        for msg in consumer:
            if msg.value:
                data = {"fields":{}}
                try:
                    msg_value = json.loads(msg.value)
                except:
                    msg_value = msg.value

