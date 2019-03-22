from kafka import KafkaConsumer
import requests
import json
import logging
import configparser
from splunk_hec_handler import SplunkHecHandler

class KafkaSplunkConnector():
    '''
    	:param conf_path: <string> path of config file
	
	conf file should contains the section 'splunk' and 'kafka'
	in splunk section:
		host, token, proto(protocol -> http/https), port, source, ssl_verify are the mandatory fields
	in kafka section:
		topic, borekers (list of brokers -> comma seperated enclosed with []), auto_offset_reset, auto_commit are mandatory fields
    '''
    def __init__(self, conf_path):
        #Splunk data
	config = configparser.ConfigParser()
        config.read(conf_path)
	splunk_data = config['splunk']
	kafka_data = config['kafka']
        self.splunk_host = splunk_data['host'] if 'host' in splunk_data.keys() else 'localhost'
        self.splunk_token = splunk_data['token'] if 'token' in splunk_data.keys() else ''
        self.splunk_port = splunk_data['port'] if 'port' in splunk_data.keys() else 8088
        self.splunk_proto = splunk_data['proto'] if 'proto' in splunk_data.keys() else 'http'
        self.splunk_source = splunk_data['source'] if 'source' in splunk_data.keys() else ''
        self.splunk_ssl_verify = splunk_data['ssl_verify'] if 'ssl_verify' in splunk_data.keys() else False

        #Kafka data
        self.kafka_topic = kafka_data['topic']
        self.kafka_brokers = [str(x.strip()) for x in kafka_data['brokers'].split(",")]
        self.kafka_auto_offset_reset = kafka_data['auto_offset_reset'] if 'auto_offset_reset' in kafka_data.keys() else 'earliest'
        self.kafka_enable_autocommit = kafka_data['auto_commit'] if 'auto_commit' in kafka_data.keys() else True

    def consume_data(self):
	'''
	Consume the data from the kafka 
	'''
	consumer = ''
	try:
	    consumer = KafkaConsumer(self.kafka_topic, bootstrap_servers = self.kafka_brokers, auto_offset_reset = self.kafka_auto_offset_reset, enable_auto_commit = self.kafka_enable_autocommit)
	except:
	    print("Error while connecting to kafka. Make sure that the details you passed is right.")
	    raise
	return consumer

    def create_logger(self):
	'''
	Create connection with splunk
	'''
	print("Creating logger..")
        logger = logging.getLogger(self.splunk_source)
        logger.setLevel(logging.INFO)
        print("Creating handler..")
	try:
            splunk_handler = SplunkHecHandler(self.splunk_host, self.splunk_token, port=self.splunk_port, proto=self.splunk_proto, ssl_verify = self.splunk_ssl_verify, source=self.splunk_source)
	except:
	    print("Error connecting with splunk. Make sure that splunk datas passed is right")
	    raise
        logger.addHandler(splunk_handler)
	return logger

    def push_record(self, data):
	'''
	Pushes a single record to the splunk
	'''
	logger = self.create_logger()
	records = {"fields":{}}
	if type(data) == dict:
            for k,v in data.items():
                records["fields"].update({str(k):v})
        else:
            records = data
	logger.info(data)
	

    def stream_to_splunk(self):
	'''
	Streams the kafka data directly to splunk
	'''
	consumer = self.consume_data()
	logger = self.create_logger()
        for msg in consumer:
            if msg.value:
                data = {"fields":{}}
                try:
                    msg_value = json.loads(msg.value)
                except:
                    msg_value = msg.value
		if type(data) == dict:
		    for k,v in msg_value.items():
	                data["fields"].update({str(k):v})
		else:
	            data = msg_value 
	        logger.info(data)
	    else:
		break
		




