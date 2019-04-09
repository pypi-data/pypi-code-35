from applauncher.kernel import ConfigurationReadyEvent
from elasticsearch import Elasticsearch, RequestsHttpConnection


class ElasticsearchBundle(object):
    def __init__(self):

        self.config_mapping = {
            "elasticsearch": {
                "hosts": "localhost",
                "use_iam": False,
                "iam_access_key": "",
                "iam_secret_key": "",
                "iam_region": ""
            }
        }
        self.injection_bindings = {}
        self.event_listeners = [
            (ConfigurationReadyEvent, self.configuration_ready)
        ]

    def configuration_ready(self, event):
        config = event.configuration.elasticsearch
        es_config = {}
        if isinstance(config.hosts, list):
            hosts = config.hosts
        else:
            hosts = [config.hosts]

        es_config["hosts"] = hosts

        if config.use_iam:
            from requests_aws4auth import AWS4Auth
            awsauth = AWS4Auth(config.iam_access_key, config.iam_secret_key, config.iam_region, 'es')
            es_config ={
                "hosts": [{'host': config.hosts, 'port': 443}],
                "http_auth": awsauth,
                "use_ssl": True,
                "verify_certs": True,
                "connection_class": RequestsHttpConnection
            }
        self.injection_bindings[Elasticsearch] = Elasticsearch(**es_config)

