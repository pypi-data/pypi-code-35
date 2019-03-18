import json
import jsonlines
import time

def load_json(path: str):
    return json.load(open(path, "r"))

def write_pretty_json(stuff, path: str):
    with open(path, 'w') as f:
        f.write(json.dumps(stuff, indent=4, sort_keys=True))

def append_pretty_json(stuff, path: str):
    with jsonlines.open(path, mode='a') as f:
        f.write(stuff)

def datetime_str():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ")

def load_jsonl(path: str):
    with jsonlines.open(path) as reader:
        return [obj for obj in reader]
