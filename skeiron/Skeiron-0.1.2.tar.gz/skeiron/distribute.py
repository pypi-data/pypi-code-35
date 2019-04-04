from skeiron.arelay import ARelay


class Distribute(ARelay):
    """
    - name: relay4  # unique name for relay
      type: distribute # [forward, echo, collect, distribute, multiply]
      topic-sub: /test/relay/4/sub
      topics-pub:
        - /test/relay/4/pub1
        - /test/relay/4/pub2
        - /test/relay/4/pub3
      active: True  # entry ignored if set to False
    """

    def __init__(self, config, mqtt_client, logger):
        ARelay.__init__(self, config, mqtt_client, logger)
        self._topics_sub.append(self._config["topic-sub"])
        for topic in self._config["topics-pub"]:
            self._topics_pub.append(topic)
        self._logger.info("Distribute.__init__ - finished initializing")
