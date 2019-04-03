from __future__ import absolute_import
from kubernetes import client, config

class MetricClient(object):

	def __init__(self):
		config.load_kube_config()
		self.v1 = client.CoreV1Api()

	def get_pods(self):
		ret = self.v1.list_pod_for_all_namespaces(watch=False)
		return ret