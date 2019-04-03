import logging

from drongo.addons.database import Database
from drongo.module import Module

from .middleware import NamespaceMiddleware


class Namespace(Module):
    """Drongo module for namespaces"""

    __default_config__ = {
        'api_base_url': '',
    }

    logger = logging.getLogger('ns')

    def init(self, config):
        self.logger.info('Initializing [ns] module.')

        self.app.context.modules.ns = self

        self.database = self.app.context.modules.database[config.database]

        if self.database.type == Database.POSTGRES:
            from .backends._postgres import services
            self.services = services

        else:
            raise NotImplementedError

        services.NSServiceBase.init(module=self)

        self.app.add_middleware(NamespaceMiddleware())

        self.init_api()

    def init_api(self):
        from .api import NamespaceAPI
        self.api = NamespaceAPI(
            app=self.app,
            module=self,
            base_url=self.config.api_base_url
        )
