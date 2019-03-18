from __future__ import print_function
import logging
import argparse
import yaml
from .importer import import_feeds_to_mysql_table


def import_feeds():
    """
    Shell command `productfeed-import` which imports feeds based on YAML configuration
    config_file (shell argument): Config file (YAML) path

    Config file example:

    tmp_dir: "/home/myuser/tmp"
    source:
      - api: "convertiser"
        config:
          token: "__MY_SECRET_TOKEN__"
          website_key: "__MY_SECRET_WEBSITE_KEY__"
          offers:
            - MY_OFFER_ID
            - ANOTHER_OFFER_ID

      - api: "webepartners"
        config:
          login: "MY_LOGIN"
          password: "MY_PASSWORD"

      - api: "mycustom_module:MyCustomImporterClass"
        config:
          my_custom: "settings"

      - api: "./my_dir/mycustom_module_file.py:MyCustomImporterClass"
        config:
          my_custom: "settings"

    destination:
      storage: 'mysql'
      config:
        host: 'MY_HOST'
        user: 'MY_USERNAME'
        passwd: 'MY_PASSWORD'
        db: 'MY_DATABASE'
        table: 'MY_TABLE'
    """
    logger_handler = logging.StreamHandler()  # Handler for the logger
    logger_handler.setFormatter(logging.Formatter('%(levelname)s [%(name)s:%(lineno)s] %(message)s'))
    logger = logging.getLogger()
    logger.addHandler(logger_handler)
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='config YAML file')
    args = parser.parse_args()
    with open(args.config_file, "r") as stream:
        settings = yaml.load(stream)
    try:
        tmp_dir = settings['tmp_dir']
    except KeyError:
        tmp_dir = ''
    storage = settings['destination']['storage']
    storage_config = settings['destination']['config']
    importers = settings['source']
    logger.info('Importers settings: %s', importers)
    logger.info('Destination settings: %s', settings['destination'])
    if storage == 'mysql':
        import_feeds_to_mysql_table(importers, storage_config, tmp_dir=tmp_dir)
    else:
        print('Storage {} not implemented'.format(storage))
