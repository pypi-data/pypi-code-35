from skeiron.arelay import ARelay


class Collect(ARelay):
    """
    - name: relay3  # unique name for relay
      type: collect # [forward, echo, collect, distribute, multiply]
      topics-sub:
        - /test/relay/3/sub1
        - /test/relay/3/sub2
        - /test/relay/3/sub3
      topic-pub: /test/relay/3/pub
      active: True  # entry ignored if set to False
    """

    def __init__(self, config, mqtt_client, logger):
        ARelay.__init__(self, config, mqtt_client, logger)
        for topic in self._config["topics-sub"]:
            self._topics_sub.append(topic)
        self._topics_pub.append(self._config["topic-pub"])
        self._logger.info("Collect.__init__ - finished initializing")
