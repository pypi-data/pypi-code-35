from .constants import DESCRIPTION, PROD_DNC_URL, VERSION
import argparse
import os
import sys


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = MyParser(prog="realvalidation", description=DESCRIPTION)

parser.add_argument('--version', '-v', action='version', version=VERSION)

parser.add_argument('--workbook', '-wb',
                    action='append',
                    help='path to workbook; you can use multiple of these',
                    required=True
                    )

parser.add_argument('--api-token', '-at',
                    default=os.environ.get('RV_TOKEN'),
                    help='real validation api_token')

parser.add_argument('--api-url', '-au',
                    help='real validation api_url; defaults to {}'
                         .format(PROD_DNC_URL),
                    default=PROD_DNC_URL,
                    )

parser.add_argument('--staging',
                    help='toggle staging api, overrides --api-url',
                    action='store_true')

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
