# -*- coding: utf-8 -*-

from logging import getLogger

from sanic import Sanic
from sanic_cors import CORS

from facture.log import LOGGING_CONFIG_DEFAULTS
from .settings import ApplicationSettings
from .error import JetErrorHandler
from .manager import jetmgr


class Application(Sanic):
    """Creates a Facture application

    :param packages: List of (<path>, <package>)
    :param path: Application root path
    :param settings: Settings overrides
    :param kwargs: kwargs to pass along to Sanic
    """

    def __init__(self, packages=None, path='/api', cors_options=None, settings=None, **kwargs):
        if not packages:
            raise Exception(f'facture.Application expects an iterable of packages, got: {type(packages)}')

        self.cors_options = cors_options or {}
        self.packages = packages

        try:
            overrides = dict(settings or {})
        except ValueError:
            raise Exception('Application `settings` must be a collection')

        for name, logger in LOGGING_CONFIG_DEFAULTS['loggers'].items():
            logger['level'] = 'DEBUG' if overrides.get('DEBUG') else 'INFO'

        super(Application, self).__init__(
            kwargs.pop('name', 'facture'),
            log_config=kwargs.pop('log_config', LOGGING_CONFIG_DEFAULTS),
            **kwargs
        )

        # Application root logger
        self.log = getLogger('root')

        # Apply known settings from ENV or provided `settings`
        self.config.update(
            ApplicationSettings(overrides, path).merged
        )

        # Set up cross-origin resource sharing
        CORS(self, supports_credentials=True, resources={r"/api/*": {"origins": "10.10.10.10"}})

        self.error_handler = JetErrorHandler()

        # Listeners
        self.register_listener(jetmgr.attach, 'after_server_start')
        self.register_listener(jetmgr.detach, 'after_server_stop')

    def run(self, host=None, port=None, workers=None, debug=False, sql_log=False, access_log=False, **kwargs):
        """Starts the HTTP server

        :param host: Listen host, defaults to 127.0.0.1
        :param port: Listen port, defaults to 8080
        :param workers: Number of workers, defaults to 1 per core.
        :param debug: Debugging
        :param sql_log: Log SQL-statements
        :param access_log: Log requests
        :param kwargs: Parameters to pass along to Sanic.run
        """

        debug = debug or self.config['DEBUG']
        workers = workers or self.config['WORKERS']

        # Enable access and sql log by default in debug mode, otherwise disable if it wasn't explicitly enabled.
        if debug:
            self.log.warning('Debug mode enabled')
            sql_log = sql_log is None or sql_log
            access_log = access_log is None or access_log

            if int(workers) > 1:
                self.log.warning('Automatic reload DISABLED due to multiple workers')

        # Configure SQL statement logging
        getLogger('peewee').setLevel('DEBUG' if sql_log else 'INFO')

        cfg = dict(
            host=host or self.config['LISTEN_HOST'],
            port=port or self.config['LISTEN_PORT'],
            workers=workers,
            debug=debug,
            access_log=access_log,
            **kwargs
        )

        self.log.info(f"Starting {cfg['workers']} worker(s) on address: {cfg['host']}:{cfg['port']}")

        super(Application, self).run(**cfg)
