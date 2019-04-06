#!/usr/bin/env python3
"""Export HOSTS that have to be excluded from patching."""
import yaml

HOSTS = []
with open("/root/.excluded_hosts.yml", 'r') as ymlfile:
    HOSTS = yaml.load(ymlfile, Loader=yaml.FullLoader)['Excluded_Hosts']
