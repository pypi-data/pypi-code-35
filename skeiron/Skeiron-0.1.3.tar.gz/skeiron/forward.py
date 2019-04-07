from skeiron.arelay import ARelay


class Forward(ARelay):
    """
    - name: relay1  # unique name for relay
      type: forward # [forward, echo, collect, distribute, multiply]
      topic-sub: /test/relay/1/sub
      topic-pub: /test/relay/1/pub
      active: True  # entry ignored if set to False
    """

    def __init__(self, config, mqtt_client, logger):
        ARelay.__init__(self, config, mqtt_client, logger)
        self._topics_sub.append(self._config["topic-sub"])
        self._topics_pub.append(self._config["topic-pub"])
        self._logger.info("Forward.__init__ - finished initializing")
