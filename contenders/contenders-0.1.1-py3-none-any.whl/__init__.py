"""Contenders: Self-hosted programming challenge framework.

Usage:
    contenders -h | --help
    contenders [--host=<host>] [--port=<port>]

Options:
    -h --help      Show this help message.
    --host=<host>  Specify the flask webserver's host.
    --port=<port>  Specify the port for the flask webserver.
"""


from docopt import docopt

from .components import app

__version__ = '0.1.0'


def main():
    arguments = docopt(__doc__, version=f'contenders {__version__}')
    port = arguments.get('--port', '80')
    host = arguments.get('--host', '127.0.0.1')
    app.run_server(port, host=host)


if __name__ == '__main__':
    main()
