from minty import Base
from minty.cqrs import CQRS
from minty.infrastructure import InfrastructureFactory

from .client import AMQPClient


class AMQPLoader(Base):
    """Loads the `AMQPClient` and inits with `CQRS` and `InfrastructureFactory`."""

    def __init__(
        self,
        domains: list,
        config_path: str,
        command_wrapper_middleware: list = None,
    ):
        """Parse config file and call setup method.

        :param Base: minty base class
        :type Base: class
        :param domains: domains to initialize in CQRS layer
        :type domains: list
        :param config_path: path to config.conf
        :type config_path: str
        :param command_wrapper_middleware: middleware to initialize , defaults to None
        :param command_wrapper_middleware: list, optional
        """
        if command_wrapper_middleware is None:
            command_wrapper_middleware = []

        self.command_wrapper_middleware = command_wrapper_middleware
        self.domains = domains
        self.config_path = config_path

        self.setup()

    def setup(self):
        """"Initializes AMQPClient with `CQRS` and `InfrastructureFactory`."""
        infra_factory = InfrastructureFactory(config_file=self.config_path)

        self.cqrs = CQRS(
            domains=self.domains,
            infrastructure_factory=infra_factory,
            command_wrapper_middleware=self.command_wrapper_middleware,
        )

        config = self.cqrs.infrastructure_factory.get_config(context=None)
        self.amqp_client = AMQPClient(
            rabbitmq_url=config["amqp"]["url"], cqrs=self.cqrs
        )
        consumers = config["amqp"]["consumer_settings"]
        if not isinstance(consumers, list):
            consumers = [consumers]
        for consumer in consumers:
            self.amqp_client.register_consumer_from_config(consumer)

    def start_client(self):
        """Start amqp client."""

        self.amqp_client.start()
