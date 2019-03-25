from spell.api import base_client
from spell.api.utils import url_path_join

CLUSTER_RESOURCE_URL = "clusters"


class ClusterClient(base_client.BaseClient):

    def get_cluster(self, cluster_id):
        """Get info for a cluster given a cluster_id.

        Keyword arguments:
        cluster_id -- the id of the cluster
        """
        r = self.request("get", url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_id))
        self.check_and_raise(r)
        return self.get_json(r)["cluster"]

    def set_kube_config(self, cluster_id, kube_config):
        """Submit a model-server kubeconfig to be stored as the
        active model-server cluster for the current org.

        Keyword arguments:
        cluster_id -- the id of the cluster to update
        ms_kube_config -- a string containing a yaml kubeconfig
        """
        payload = {"kube_config": kube_config}
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_id, "kube_config")
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)
