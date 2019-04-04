import pelops.mylogger
import skeiron.forward
import skeiron.echo
import skeiron.collect
import skeiron.distribute
import skeiron.multiply

"""


"""


class RelayFactory:
    """
    Relay class - creates silblings from AElement based on the provided config yaml structure.

    config yaml - everything from arelay siblings and:
        type: multiply # [forward, echo, collect, distribute, multiply]
        active: True  # entry ignored if set to False
    """

    @staticmethod
    def create_relay(config, mqtt_client, logger):
        """
        Create the element that corresponds to the provided config yaml.

        :param config: config yaml structure for a single element
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance
        :return: instance of the created element
        """
        _logger = pelops.mylogger.get_child(logger, __name__)
        relay = None
        if config["active"]:
            if config["type"].lower() == "forward":
                relay = skeiron.forward.Forward(config, mqtt_client, logger)
            elif config["type"].lower() == "echo":
                relay = skeiron.echo.Echo(config, mqtt_client, logger)
            elif config["type"].lower() == "collect":
                relay = skeiron.collect.Collect(config, mqtt_client, logger)
            elif config["type"].lower() == "distribute":
                relay = skeiron.distribute.Distribute(config, mqtt_client, logger)
            elif config["type"].lower() == "multiply":
                relay = skeiron.multiply.Multiply(config, mqtt_client, logger)
            else:
                _logger.error("RelayFactory.create_relay - unknown behavior '{}'".
                              format(config["type"].lower()))
                raise ValueError("RelayFactory.create_relay - unknown behavior '{}'".
                                 format(config["type"].lower()))
        else:
            _logger.info("RelayFactory.create_relay - skipping inactive element '{}.{}'.".
                      format(config["type"].lower(), config["name"]))

        return relay

    @staticmethod
    def create_relay_list(configs, mqtt_client, logger):
        """
        Create all relays that are defined in the provided config.

        :param configs: config yaml for timer (array)
        :param mqtt_client: mymqttclient instance
        :param logger: logger instance
        :return: list of all active elements
        """
        relay_list = []
        _logger = pelops.mylogger.get_child(logger, __name__)

        _logger.info("RelayFactory.create_controller - start")

        for config in configs:
            relay = RelayFactory.create_relay(config, mqtt_client, logger)
            if relay is not None:
                relay_list.append(relay)

        _logger.info("RelayFactory.create_controller - created {} controller.".format(len(relay_list)))
        _logger.info("RelayFactory.create_controller - finished")

        return relay_list

