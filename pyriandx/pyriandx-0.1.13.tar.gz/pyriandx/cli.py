from docopt import docopt
import sys
import os
import logging as log

from pyriandx.log import *


from . import __title__, __version__, __description__, PROG

__doc__ = f'''

{__title__} ::: {__description__}

Usage: 
   {PROG} [-hxv] [--username <username>] [--password <password>] [--output-dir <output-dir>] --institution <institution> --json <json-file> <target-vcf>

Options:
   -h, --help                      Prints this help and exit
   -v, --version                   Prints the version and exits
   -b, --base_url                  Base URL for PierianDX service [default: https://app.uat.pieriandx.com/cgw-api/v2.0.0].
   -u, --username=username         Username for PierianDX service, usually an email address. Overrides environment if it exists.
   -p, --password=password         Password for PierianDX service. Overrides environment if it exists.
   -j, --json                      JSON file with details for target
   -i, --institution=institution   Institution to use for API authentication
   -o, --output-dir=output-dir     Directory to place downloaded reports. [default: output]
   -x, --verbose                   Make output more verbose innit
   

Environment variables:
   DEBUG_HTTP         If defined, prints verbose information for all http transactions
   USERNAME           If defined, uses this as username for authenticating to PierianDX
   PASSWORD           If defined, uses this as password for authenticating to PierianDX
   BASE_URL           If defined, uses this as base URL for PierianDX service
'''

def parse_args(argv=sys.argv[1:]):
   version = f'{__title__} (version {__version__})'
   args = docopt(__doc__, argv, help=True, version=version)

   if os.environ.get('USERNAME') and not args['--username']:
      args['--username'] = os.environ.get('USERNAME')
   
   if os.environ.get('PASSWORD') and not args['--password']:
      args['--password'] = os.environ.get('PASSWORD')

   if not args['--username']:
      print(__doc__)
      print(colored("Please provide a username via --username flag or USERNAME environment variable.\n",'red'))

   if not args['--password']:
      print(__doc__)
      print(colored("Please provide a password via --password flag or PASSWORD environment variable.\n",'red'))

      
   return args
