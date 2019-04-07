from skeiron.arelay import ARelay


class Echo(ARelay):
    """
    - name: relay2  # unique name for relay
      type: echo # [forward, echo, collect, distribute, multiply]
      topic: /test/relay/2
      active: True  # entry ignored if set to False
    """

    def __init__(self, config, mqtt_client, logger):
        ARelay.__init__(self, config, mqtt_client, logger)
        self._topics_sub.append(self._config["topic"])
        self._topics_pub.append(self._config["topic"])
        self._logger.info("Echo.__init__ - finished initializing")
