import argparse
import importlib

from drongo.nest import Nest

__all__ = ['main']


def _parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('app', help='py.module:app_instance')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=8000, type=int)
    parser.add_argument('--auto-reload', action='store_true')
    parser.add_argument('--asyncio', action='store_true', default=False)
    parser.add_argument('--log', action='store_true')
    return parser.parse_args()


def main():
    options = _parse()

    if options.log:
        import logging
        fmt = (
            '\033[36m%(asctime)-24s \033[34m%(name)-16s '
            '\033[32m%(levelname)-8s \033[97m%(message)s\033[39m'
        )
        logging.basicConfig(format=fmt, level=logging.INFO)

    module, app = options.app.split(':')
    module = importlib.import_module(module)
    app = getattr(module, app)

    kwargs = dict(
        app=app,
        host=options.host,
        port=options.port,
        auto_reload=options.auto_reload,
        asyncio=options.asyncio
    )
    nest = Nest(**kwargs)
    try:
        nest.run()
    except KeyboardInterrupt:
        print('Exiting...')
        nest.shutdown()


if __name__ == '__main__':
    main()
