import sys
import argparse
import requests
import json
from .user_agents import *

ua_map = {
    'default': UA_GOOGLEBOT,
    'desktop': UA_GOOGLEBOT,
    'googlebot': UA_GOOGLEBOT,
    'mobile': UA_GOOGLEBOT_SMARTPHONE,
    'googlebot-mobile': UA_GOOGLEBOT_SMARTPHONE,
    'googlebot2': UA_GOOGLEBOT2,
    'bingbot': UA_BINGBOT,
    'bingbot-mobile': UA_BINGBOT_IPHONE,
    'browser': UA_BROWSER,
    'iphone': UA_BROWSER,
    'pixel': UA_PIXEL,
}

ua_help = "ROBOT_AGENT should be one of the following values (default: 'googlebot'):\n%s" % ", ".join(ua_map.keys())

def main(argv=None):
    parser = argparse.ArgumentParser(description="Fetch URLs as search engine robot.")
    parser.add_argument('url')
    parser.add_argument('-r', '--follow-redirects', action='store_true', help="Follow redirects, if any occur")
    parser.add_argument('-I', '--headers', action='store_true', help="Show only response headers")
    parser.add_argument('-a', '--robot-agent', default='default', help=ua_help)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args(argv)

        if not args.robot_agent in ua_map:
            print(ua_help)
            sys.exit(1)

        payload = {
            'headers': {
                'user-agent': ua_map.get(args.robot_agent)
            },
            'verify': False,
            'allow_redirects': args.follow_redirects,
        }

        try:
            r = requests.get(args.url, **payload)
            if args.headers:
                print(json.dumps(dict(r.headers), indent=2))
            else:
                print(r.text)
        except KeyboardInterrupt:
            sys.exit()


if __name__ == "__main__":
    main()
