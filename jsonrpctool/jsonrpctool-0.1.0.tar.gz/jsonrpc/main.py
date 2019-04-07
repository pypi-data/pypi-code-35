import os
import re
import sys
import json
import argparse
from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.exceptions import ReceivedErrorResponseError


ENDPOINT_ENV = 'JSONRPC_ENDPOINT'


def main(args=sys.argv[1:]):
    """
    Commandline JSON-RPC client tool.
    """
    (endpoint, method, listparams, dictparams) = parse_args(args)
    client = HTTPClient(endpoint, basic_logging=False)
    try:
        response = client.request(method, *listparams, **dictparams)
    except ReceivedErrorResponseError as e:
        raise SystemExit(str(e))
    else:
        json.dump(response.data.result, sys.stdout, sort_keys=True, indent=2)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    epdef = os.environ.get(ENDPOINT_ENV)
    p.add_argument(
        '--endpoint',
        dest='ENDPOINT',
        default=epdef,
        help=(
            'JSON-RPC endpoint, defaults to {} environment variable: {}'
            .format(
                ENDPOINT_ENV,
                'not defined' if epdef is None else repr(epdef),
            )
        ),
    )
    p.add_argument('METHOD')
    p.add_argument('PARAMS', nargs='*')
    opts = p.parse_args(args)

    if opts.ENDPOINT is None:
        p.error(
            'No endpoint supplied with --endpoint or {} environment variable.'
            .format(ENDPOINT_ENV)
        )

    listparams = []
    dictparams = {}
    paramtype = None

    for param in opts.PARAMS:
        m = re.match(r'((?P<KEY>[a-zA-Z0-9_]+)=)?(?P<VALUE>.*)$', param)
        if m is None:
            p.error('Could not parse: {!r}'.format(param))
        else:
            key = m.group('KEY')
            if key is None:
                newparamtype = 'array'
            else:
                newparamtype = 'object'

            if paramtype is None:
                paramtype = newparamtype
            elif newparamtype != paramtype:
                p.error('Cannot mix array and object params.')

            value = m.group('VALUE')
            try:
                value = json.loads(value)
            except ValueError:
                pass

            if paramtype == 'array':
                listparams.append(value)
            else:
                dictparams[key] = value

    return (opts.ENDPOINT, opts.METHOD, listparams, dictparams)
