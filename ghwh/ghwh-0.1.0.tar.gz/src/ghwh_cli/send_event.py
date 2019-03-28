from argparse import ArgumentParser

from requests import post

from ghwh_data import load


def get_headers(event):
    headers = {
        "X-GitHub-Event": event,
        "X-GitHub-Delivery": "72d3162e-cc78-11e3-81ab-4c9367dc0958",
        "X-Hub-Signature": "sha1=7d38cdd689735b008b3c702edd92eea23791c5f6",
    }
    return headers


def argparser(args=None):
    p = ArgumentParser()
    p.add_argument("event", nargs="?", choices=("push",), default="push")
    p.add_argument("--endpoint", default="http://localhost:5000/webhook")
    return p


def main(args=None):
    parser = argparser()
    args = parser.parse_args(args=args)
    event = args.event
    endpoint = args.endpoint
    headers = get_headers(event)
    payload = load(event + ".json")
    resp = post(endpoint, json=payload, headers=headers)
    print(resp)
