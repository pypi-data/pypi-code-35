import logging

from drongo.addons.database import Database
from drongo.module import Module


class Auth(Module):
    """Drongo module for authentication and authorization"""

    __default_config__ = {
        'api_base_url': '',

        'create_admin_user': True,
        'admin_user': 'admin',
        'admin_password': 'admin',

        'active_on_register': False,

        'token_secret': 'drongo.auth.secret',
        'token_age': 7 * 24 * 60 * 60,  # A week (in seconds)
    }

    logger = logging.getLogger('auth')

    def init(self, config):
        self.logger.info('Initializing [auth] module.')

        self.app.context.modules.auth = self

        self.database = self.app.context.modules.database[config.database]

        if self.database.type == Database.POSTGRES:
            from .backends._postgres import services
            self.services = services

        else:
            raise NotImplementedError

        services.AuthServiceBase.init(module=self)

        if config.create_admin_user:
            svc = services.UserCreate(
                username=config.admin_user,
                password=config.admin_password,
                is_active=True,
                is_superuser=True
            )
            if not svc.check_exists():
                svc.call()

        self.init_api()

    def init_api(self):
        from .api import AuthAPI
        self.api = AuthAPI(
            app=self.app,
            module=self,
            base_url=self.config.api_base_url
        )
