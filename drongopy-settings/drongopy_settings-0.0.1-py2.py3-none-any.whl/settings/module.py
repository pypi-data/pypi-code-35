import logging

from drongo.addons.database import Database
from drongo.module import Module


class Settings(Module):
    """Drongo module for module settings"""

    __default_config__ = {
        'api_base_url': '',
    }

    logger = logging.getLogger('settings')

    def init(self, config):
        self.logger.info('Initializing [settings] module.')

        self.app.context.modules.settings = self

        self.database = self.app.context.modules.database[config.database]

        if self.database.type == Database.POSTGRES:
            from .backends._postgres import services
            self.services = services

        else:
            raise NotImplementedError

        services.SettingsServiceBase.init(module=self)
        self.init_api()

    def init_api(self):
        from .api import SettingsAPI
        self.api = SettingsAPI(
            app=self.app,
            module=self,
            base_url=self.config.api_base_url
        )
