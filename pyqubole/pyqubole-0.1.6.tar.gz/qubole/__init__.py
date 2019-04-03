#!/usr/bin/env python
"""Basic Qubole Functionality
"""
import json
import os
import pprint

import requests

__version__ = "0.1.6"

class Qubole:
    """Basic qubole wrapper"""
    def __init__(self):
        try:
            self.token = os.environ["QUBOLE_TOKEN"]
        except KeyError:
            print("Qubole Token: MISSING")
        self.api = "https://us.qubole.com/api/v1.3/clusters/{CLUSTERID}/state"
        self.active = None

    def state(self, cluster, full=False):
        """Finds out the state of the cluster"""
        response = requests.get(
            url=self.api.format(CLUSTERID=cluster),
            headers={'X-AUTH-TOKEN': self.token}
        )

        values = json.loads(response.content)
        try:
            if full:
                pprint.pprint(values)
            else:
                if values["state"] == 'UP':
                    print(f"Cluster {cluster} UP")
                    self.active = True
                    print('Ganglia: https://us.qubole.com/ganglia-metrics-{clusterid}/'.format(clusterid = values["cluster_id"]))
                elif values["state"] == 'DOWN':
                    print(f"Cluster {cluster} DOWN")
                    self.active = False
                elif values["state"] == "PENDING":
                    print(f"Cluster {cluster} PENDING")
                    self.active = False
                else:
                    print(f"Cluster {cluster} UNKNOWN")
                    self.active = False
        except:
            print(values)


    def toggle(self, cluster):
        """Toggles the cluster on and off"""
        self.state(cluster)
        state = "start" if not self.active else "terminate"
        response = requests.put(
            url=self.api.format(CLUSTERID=cluster),
            headers={
                'X-AUTH-TOKEN': self.token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            data=json.dumps({"state": state})
        )
        try:
            pprint.pprint(json.loads(response.content))
        except TypeError as e:
            print(f"Error: {e}")
