import logging
import os
from abc import ABCMeta

from aws_xray_sdk.core import patch_all

from lambdabase.ConfigManager import ConfigManager
from lambdabase.Constants import Constants
from lambdabase.log.LogFactoryBase import LogFactoryBase as LogFactory


class BaseStrap(object):
    """
    Base class for all lambda bootstraps
    """
    __metaclass__ = ABCMeta

    services = {}
    config_manager = ConfigManager()

    def __init__(self):
        self.logger = logging.getLogger(BaseStrap.__class__.__name__)
        self.logger.info(LogFactory.base_006())
        environment = os.environ['environment'] \
            if 'environment' in os.environ \
            else Constants.LOCAL_ENVIRONMENT_KEY
        self.config_manager.load('config', environment)
        self.setup_tracing(environment)

    @property
    def config(self):
        return self.config_manager

    def get_service(self, service_type):
        """
        Gets the singleton service of the specified type. If there is no
        match for the exact type then look for subclasses of the requested
        type. If there are multiple registered subclasses or there is no
        match at all then raise a BootstrapException
        :param service_type: the type of the service to return
        :return: The singleton instance of the service specified type
        """
        self.logger.info(LogFactory.base_007(service_type))

        if service_type in self.services:
            service = self.services[service_type]
        else:
            subclasses = [x for x in self.services if issubclass(x, service_type)]

            if len(subclasses) == 0:
                raise BootstrapException("Unable to find the specified service type")
            if len(subclasses) > 1:
                raise BootstrapException("Found multiple registered subclasses of the same type")
            service = subclasses[0]

        self.logger.info(LogFactory.base_008(type(service), service_type))

        return service

    def register(self, service):
        """
        Register the specified service
        :param service: An initialised singleton service
        """
        service_type = type(service)
        if service_type in self.services:
            raise BootstrapException("Service type has already been registered")
        self.services[service_type] = service
        self.logger.info(LogFactory.base_009(service_type.__module__))

    @classmethod
    def setup_tracing(cls, environment):
        """
        Patches various standard python libraries for use with x-ray.
        Libraries are only patched when running local
        """
        if environment != Constants.LOCAL_ENVIRONMENT_KEY:
            patch_all()


class BootstrapException(StandardError):
    pass
