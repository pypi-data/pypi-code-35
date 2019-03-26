import logging
import time
import toml
import sys
import os.path
from statsd_mangler import StatsdListener
from statsd_mangler import StatsdSender
from statsd_mangler import Mangler

def main():
    if len(sys.argv) < 2:
        print("statsd_mangler <statsd_mangler.toml>")
        exit(1)
    configFile = sys.argv[1]
    if not os.path.isfile(configFile):
        print("Config file {} not found".format(configFile))
    config = toml.load(configFile)
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    logging.getLogger().setLevel(config["log"]["level"])
    logging.info("Starting up")
    logging.debug("Config loaded: %s", config)

    sender = StatsdSender(config["destination"]["host"], config["destination"]["port"])
    mangler = Mangler(config["patterns"], sender)
    listener = StatsdListener(config["listen"]["port"], mangler)

    while True:
        try:
            listener.listen()
        except Exception:
            logging.exception(Exception)
            time.sleep(10)

if __name__ == '__main__':
    main()
