import pelops.logging.mylogger
import thyestes.restarttimer
import thyestes.spawntimer


"""


"""


class TimerFactory:
    """
    Factory class - creates silblings from AElement based on the provided config yaml structure.

    config yaml - everything from acontroller and:
        on-new-command-behavior: restart  # [restart, spawn] - should the same timer be restarted (there is only one
                                            timer and it will be resetted) or should a new timer be spawned (the
                                            previous timer continous to count down untouched).
        active: True  # entry ignored if set to False
    """

    @staticmethod
    def create_controller(config, mqtt_client, logger):
        """
        Create the element that corresponds to the provided config yaml.

        :param config: config yaml structure for a single element
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance
        :return: instance of the created element
        """
        _logger = pelops.logging.mylogger.get_child(logger, __name__)
        controller = None
        if config["active"]:
            if config["on-new-command-behavior"].lower() == "spawn":
                controller = thyestes.spawntimer.SpawnTimer(config, mqtt_client, logger)
            elif config["on-new-command-behavior"].lower() == "restart":
                controller = thyestes.restarttimer.RestartTimer(config, mqtt_client, logger)
            else:
                _logger.error("TimerFactory.create_controller - unknown behavior '{}'".
                              format(config["on-new-command-behavior"].lower()))
                raise ValueError("TimerFactory.create_controller - unknown behavior '{}'".
                                 format(config["on-new-command-behavior"].lower()))
        else:
            _logger.info("TimerFactory.create_controller - skipping inactive element '{}.{}'.".
                      format(config["on-new-command-behavior"].lower(), config["name"]))

        return controller

    @staticmethod
    def create_controller_list(configs, mqtt_client, logger):
        """
        Create all controller that are defined in the provided config.

        :param configs: config yaml for timer (array)
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance
        :return: list of all active elements
        """
        controller_list = []
        _logger = pelops.logging.mylogger.get_child(logger, __name__)

        _logger.info("TimerFactory.create_controller - start")

        for config in configs:
            controller = TimerFactory.create_controller(config, mqtt_client, logger)
            if controller is not None:
                controller_list.append(controller)

        _logger.info("TimerFactory.create_controller - created {} controller.".format(len(controller_list)))
        _logger.info("TimerFactory.create_controller - finished")

        return controller_list

