from skeiron.arelay import ARelay


class Multiply(ARelay):
    """
    - name: relay5  # unique name for relay
      type: multiply # [forward, echo, collect, distribute, multiply]
      topics-sub:
        - /test/relay/5/sub1
        - /test/relay/5/sub2
        - /test/relay/5/sub3
      topics-pub:
        - /test/relay/5/pub1
        - /test/relay/5/pub2
        - /test/relay/5/pub3
      active: True  # entry ignored if set to False
    """

    def __init__(self, config, mqtt_client, logger):
        ARelay.__init__(self, config, mqtt_client, logger)
        for topic in self._config["topics-sub"]:
            self._topics_sub.append(topic)
        for topic in self._config["topics-pub"]:
            self._topics_pub.append(topic)
        self._logger.info("Multiply.__init__ - finished initializing")
