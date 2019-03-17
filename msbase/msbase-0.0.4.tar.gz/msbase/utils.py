import json
import time

def load_json(p: str):
    return json.load(open(p, "r"))

def write_pretty_json(stuff, path: str):
    open(path, 'w').write(json.dumps(stuff, indent=4, sort_keys=True))

def datetime_str():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ")
