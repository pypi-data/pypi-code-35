# -*- coding: utf-8 -*-

from os import getpid
import inspect

import aiohttp
# from sanic_cors import CORS

from facture.core.package import Jetpack
from facture.utils import format_path
from facture.db import Database


class JetManager:
    """Takes care of package registration and injection upon application start"""

    pkgs = []
    sanic = None
    loop = None
    db = Database
    http_client: aiohttp.ClientSession

    @property
    def models(self):
        """Yields a list of package-model tuples"""

        for pkg_name, pkg in self.pkgs:
            for model in pkg.models:
                yield pkg, model

    def get_pkg(self, name):
        """Get package by name"""

        return dict(self.pkgs).get(name)

    def _load_packages(self, pkg_modules: list):
        """Takes a list of Jetpacks, tests their sanity and registers with manager"""

        for assigned_path, module in pkg_modules:
            if not hasattr(module, 'export'):
                raise Exception(f'Missing package export in {module}')
            elif not isinstance(module.export, Jetpack):
                raise Exception(f'Invalid package type {module.pkg}: must be of type {Jetpack}')

            export = module.export
            if export.name in dict(self.pkgs).keys():
                raise Exception(f'Duplicate package name {export.name}')

            export.version = getattr(module, '__version__', '0.0.0')
            export.path = assigned_path
            export.log.debug(f'Loading version {export.version}')
            self.pkgs.append((export.name, export))

    async def _register_services(self):
        """Registers Services with Application"""

        for pkg_name, pkg in self.pkgs:
            for svc in pkg.services:
                # Make package available to Controller
                svc.register(pkg, self)
                svc_obj = svc()

                if inspect.iscoroutinefunction(svc_obj.on_ready):
                    await svc_obj.on_ready()
                else:
                    svc_obj.on_ready()

                pkg.log.info(f'Service {svc.__name__} initialized')

    def _register_models(self):
        """Registers Models with the application, and creates non-existent tables"""

        models = list(self.models)
        registered = []

        if models and not self.db.connection:
            raise Exception('Unable to register models without a database connection')

        for pkg, model in models:
            if not hasattr(model, 'Meta'):
                meta = type('ModelMeta', (object, ), {})
                model.Meta = meta

            # Inject model meta and set its namespace
            meta = model._meta
            meta.database = self.db.connection
            meta.table_name = f'{pkg.name}__{meta.table_name}'

            pkg.log.debug(f'Registering model: {model.__name__} [{meta.table_name}]')

            registered.append(model)

        with self.db.connection.allow_sync():
            self.db.connection.create_tables(registered, safe=True)

    async def _register_controllers(self):
        """Registers Controllers with Application"""

        for pkg_name, pkg in self.pkgs:
            pkg.log.info('Controller initializing')
            path_base = self.sanic.config['API_BASE']

            # Make package available to Controller
            pkg.controller.register(pkg)
            ctrl = pkg.controller = pkg.controller()

            # Iterate over route stacks and register routes with the application
            for handler, route in ctrl.stacks:
                handler_addr = hex(id(handler))
                handler_name = f'{pkg_name}.{route.name}'
                path_full = format_path(path_base, pkg.path, route.path)
                pkg.log.debug(
                    f'Registering route: {path_full} [{route.method}] => '
                    f'{route.name} [{handler_addr}]'
                )

                # Register with Sanic
                self.sanic.route(
                    uri=path_full,
                    methods=frozenset({route.method}),
                    host=None,
                    strict_slashes=False,
                    stream=None,
                    version=None,
                    name=handler_name,
                )(handler)

                # Inject full path to route handler
                route.path_full = path_full

            # Let the Controller know we're ready to receive requests
            if inspect.iscoroutinefunction(ctrl.on_ready):
                await ctrl.on_ready()
            else:
                ctrl.on_ready()

            pkg.log.info('Controller initialized')

    def register_cors(self):
        cors_options = self.sanic.cors_options or {}
        # CORS(self.sanic, **cors_options)

    async def detach(self, *_):
        """Application stop-handler"""

        await self.http_client.close()

    async def attach(self, app, loop):
        """Application start-handler

        Sets up DB and HTTP clients, followed by component registration.

        :param app: Instance of facture.Application
        :param loop: Instance of `uvloop.Loop`
        """

        self._load_packages(app.packages)
        self.sanic = app
        self.loop = loop

        self.http_client = aiohttp.ClientSession(loop=loop)
        if app.config['DB_URL']:
            self.db.register(app, loop)
            self._register_models()

        await self._register_controllers()
        await self._register_services()

        app.log.info(f'Worker {getpid()} ready for action')


jetmgr = JetManager()
