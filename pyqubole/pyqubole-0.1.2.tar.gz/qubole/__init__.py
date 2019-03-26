#!/usr/bin/env python
"""Basic Qubole Functionality
"""
import json
import os

import requests


class Qubole:
    """Basic qubole wrapper"""
    def __init__(self):
        try:
            self.token = os.environ["QUBOLE_TOKEN"]
        except KeyError:
            print("Qubole Token: MISSING")
        self.api = "https://us.qubole.com/api/v1.3/clusters/{CLUSTERID}/state"

    def state(self, cluster, full=False):
        """Finds out the state of the cluster"""
        response = requests.get(
            url=self.api.format(CLUSTERID=cluster),
            headers={'X-AUTH-TOKEN': self.token}
        )

        values = json.loads(response.content)
        if full:
            print(values)
        else:
            if values["state"] == 'UP':
                print(f"Cluster {cluster} UP")
                state = True
            elif values["state"] == 'DOWN':
                print(f"Cluser {cluster} DOWN")
                state = False
            elif values["state"] == "PENDING":
                print(f"Cluster {cluster} PENDING")
                state = False
            else:
                print(f"Cluster {cluster} UNKNOWN")
                state = False
            return state

    def toggle(self, cluster):
        """Toggles the cluster on and off"""
        active = self.state(cluster)
        state = "start" if not active else "terminate"
        response = requests.put(
            url=self.api.format(CLUSTERID=cluster),
            headers={
                'X-AUTH-TOKEN': self.token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            data=json.dumps({"state": state})
        )
        print(response.content)

