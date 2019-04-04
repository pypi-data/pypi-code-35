from pelops.abstractmicroservice import AbstractMicroservice
from lysidike.services.servicefactory import ServiceFactory
from lysidike.tasks.taskfactory import TaskFactory
from lysidike.schema.publishgateway import get_schema
import lysidike


class PublishGateway(AbstractMicroservice):
    """
    Provides the possibility to publish aggregated mqtt messages to various services. Several tasks listen to
    incoming messages, render messages and publishes them to the service.

    config yaml structure
    mqtt:
        mqtt-address: localhost
        mqtt-port: 1883
        credentials-file: ~/credentials.yaml
        log-level: WARNING

    logger:
        log-level: DEBUG
        log-file: lysidike.log

    publish-gateway:
        services:
            email:
                address: smtp.zoho.com
                port: 465
                from: name123@sender123.com
                to: name123@receiver123.com
                credentials-file: ~/credentials.yaml
            stdout:
                prefix: ------------------------------------------------------------------------------
                suffix: ..............................................................................
        tasks:
          - name: collection
            service: stdout  # [email, stdout, ...] one of the services
            subject: sending collected messages  # subject for message
            every-nth-message: 10  # collect this amount of messages before publishing them. 0 for never
            every-nth-second: 10  # wait this time before publishing all messages that are waiting. 0 for never
            topics-sub:
                - /test/a
                - /test/b
          - name: ...

    """
    _version = lysidike.version

    _services = None  # list of services
    _tasks = None  # list of tasks

    def __init__(self, config, mqtt_client=None, logger=None, stdout_log_level=None, no_gui=None):
        """
        Constructor - creates the services and the tasks

        :param config: config yaml structure
        :param mqtt_client: mqtt client instance
        :param logger: logger instance
        :param no_gui: if False create and control a ui instance
        :param stdout_log_level: if set, a logging handler with target sys.stdout will be added
        """
        AbstractMicroservice.__init__(self, config, "publish-gateway", mqtt_client, logger,
                                      stdout_log_level=stdout_log_level, no_gui=no_gui)
        self._services = ServiceFactory.get_services(self._config["services"], self._mqtt_client, self._logger)
        self._tasks = TaskFactory.get_tasks(self._config["tasks"], self._services, self._mqtt_client, self._logger)

    def _start(self):
        self._logger.info("PublishGateway._start - starting services")
        for service in self._services.values():
            service.start()
        self._logger.info("PublishGateway._start - starting tasks")
        for task in self._tasks.values():
            task.start()
        self._logger.info("PublishGateway._start - finished")

    def _stop(self):
        self._logger.info("PublishGateway._stop - stopping tasks")
        for task in self._tasks.values():
            task.stop()
        self._logger.info("PublishGateway._stop - stopping services")
        for service in self._services.values():
            service.stop()
        self._logger.info("PublishGateway._stop - finished")

    @classmethod
    def _get_description(cls):
        return "Lysidike publishes incoming mqtt messages to various internet services like email."

    @classmethod
    def _get_schema(cls):
        return get_schema()

    def runtime_information(self):
        return {}

    def config_information(self):
        return {}


def standalone():
    PublishGateway.standalone()


if __name__ == "__main__":
    PublishGateway.standalone()
