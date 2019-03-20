#!/usr/bin/env python

import json
import requests
import pprint

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

address = "https://localhost:7777/"

# Pull data
payload = {
    "meta": {
        "name": "testing_manager",
        "tag": None,
        "limit": 1
    },
    "data": {}
}
r   = requests.get(address + "queue_manager", json=payload, verify=False)
tmp = r.json()

pprint.pprint(tmp)

