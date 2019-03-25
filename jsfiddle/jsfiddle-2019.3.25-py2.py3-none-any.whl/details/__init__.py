#!/usr/bin/env python
import os
import public
import ruamel.yaml as yaml


@public.add
def load():
    """return a dictorinary with `demo.details` data"""
    path = os.path.join(os.getcwd(), "demo.details")
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as stream:
        return yaml.load(stream, Loader=yaml.Loader)


@public.add
def save(data):
    """save a dictionary to a `demo.details` file"""
    path = os.path.join(os.getcwd(), "demo.details")
    if "resources" in data and not data.get("resources",[]):
        del data["resources"]
    with open(path, 'w') as outfile:
        yaml.dump(data, outfile, Dumper=yaml.RoundTripDumper)
