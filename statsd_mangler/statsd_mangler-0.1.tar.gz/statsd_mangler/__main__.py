import logging
import time
import toml
from statsd_mangler import StatsdListener
from statsd_mangler import StatsdSender
from statsd_mangler import Mangler

def main():
    config = toml.load('statsd_mangler.toml')
    logging.basicConfig(
        filename=config['log']['destination'],
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
