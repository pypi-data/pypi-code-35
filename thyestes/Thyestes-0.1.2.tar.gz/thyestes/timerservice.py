from pelops.abstractmicroservice import AbstractMicroservice
import thyestes
import thyestes.schema.schema
import thyestes.timerfactory


class Timerservice(AbstractMicroservice):
    _version = thyestes.version
    _controller = None

    def __init__(self, config, mqtt_client=None, logger=None, stdout_log_level=None, no_gui=None):
        """
        Constructor - creates the services and the tasks

        :param config: config yaml structure
        :param mqtt_client: mqtt client instance
        :param logger: logger instance
        :param no_gui: if False create and control a ui instance
        :param stdout_log_level: if set, a logging handler with target sys.stdout will be added
        """
        AbstractMicroservice.__init__(self, config, "timerservice", mqtt_client, logger,
                                      stdout_log_level=stdout_log_level, no_gui=no_gui)
        self._controller = thyestes.timerfactory.TimerFactory.create_controller_list(self._config, self._mqtt_client,
                                                                                     self._logger)

    def _start(self):
        for controller in self._controller:
            controller.start()

    def _stop(self):
        for controller in self._controller:
            controller.stop()

    @classmethod
    def _get_description(cls):
        return "Thyestes it a timer microservice. Listens on topics for specific messages, starts a timer when such " \
               "a messages has been received and publishes a predefined message after the timer expired."

    @classmethod
    def _get_schema(cls):
        """
        Get the sub schema to validate the yaml-config file against.

        :return: json-schema dict
        """
        return thyestes.schema.schema.get_schema()

    def runtime_information(self):
        return {}

    def config_information(self):
        return {}


def standalone():
    Timerservice.standalone()


if __name__ == "__main__":
    Timerservice.standalone()
