#! /usr/bin/env python

import argparse
import json
import logging
import os
import requests
import sys
import urllib3


urllib3.disable_warnings()


class ElasticsearchConnector:
    def __init__(self, logger, use_ssl, hostname, port, cacert, cert, key):
        self.logger = logger
        if cacert:
            self.verify = cacert
        else:
            self.verify = False
        self.cert = cert
        self.key = key
        if use_ssl:
            self.url_base = 'https://'
        else:
            self.url_base = 'http://'

        self.url_base += f'{hostname}:{port}'

    def head(self, path):
        return requests.head(self.url_base + f'/{path}',
                             cert=(self.cert, self.key),
                             verify=self.verify)

    def put(self, path, put_data):
        return requests.put(self.url_base + f'/{path}',
                            cert=(self.cert, self.key),
                            verify=self.verify,
                            json=put_data)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--template-directory',
                        dest='template_directory', required=True,
                        help=('The path to the directory containing the index'
                              ' template files'))
    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='Enable debug logigng')
    parser.add_argument('--es-use-ssl', default=False, action='store_true',
                        help='Use SSL/TLS when connecting to Elasticsearch')
    parser.add_argument('--es-hostname', required=True,
                        help=('The Elasticsearch hostname. Do not prefix '
                              'with http/https'))
    parser.add_argument('--es-port', required=True,
                        help='The Elasticsearch port number')
    parser.add_argument('--es-cacert', default=None,
                        help=('The path to a CA certificate file for verifying'
                              ' the Elasticsearch server authenticity'))
    parser.add_argument('--es-cert', default=None,
                        help=('The path to a cert file for authenticating to'
                              ' Elasticsearch'))
    parser.add_argument('--es-key', default=None,
                        help=('The path to a key file for authenticating to'
                              ' Elasticsearch'))
    parser.add_argument('--overwrite-templates', default=False,
                        action='store_true',
                        help='Overwrite any templates that already exist')
    return parser.parse_args()


def setup_logging(debug):
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger


def load_template(logger, template_path):
    with open(template_path) as t:
        template_data = json.loads(t.read())
    template_name = os.path.basename(template_path)
    logger.debug(f'Loaded template data from {template_path}')
    return (template_name, template_data)


def template_exists(logger, es, template_name):
    logger.debug(f'Checking if template "{template_name}" exists')
    status_code = es.head(f'_template/{template_name}').status_code
    if status_code == 404:
        return False
    elif status_code == 200:
        return True
    else:
        logger.exception((f'Unexpected status code "{status_code}" received'
                          f' when checking if template "{template_name}"'
                          ' exists. Exiting.'))
        sys.exit(1)


def apply_template(logger, es, overwrite, template_name, template_data):
    exists = template_exists(logger, es, template_name)
    if exists and not overwrite:
        logger.exception((f'A template with the name "{template_name}"'
                          ' already exists. If you wish to overwrite it, run'
                          ' the script with the "--overwrite-templates"'
                          ' argument. Exiting.'))
        sys.exit(1)
    else:
        logger.debug(f'Creating template "{template_name}"')
        r = es.put(f'_template/{template_name}', template_data)
        if r.status_code != 200:
            logger.exception(('Erorr when creating template '
                              f'"{template_name}": {r.text}'))
            sys.exit(1)


def main():
    args = parse_args()
    logger = setup_logging(args.debug)
    es = ElasticsearchConnector(logger, args.es_use_ssl, args.es_hostname,
                                args.es_port, args.es_cacert, args.es_cert,
                                args.es_key)
    if not os.path.isdir(args.template_directory):
        logger.exception(('The specified template directory '
                          f'"{args.template_directory}" does '
                          'not exist. Exiting.'))
        sys.exit(1)

    templates = {}
    template_directory = os.listdir(args.template_directory)
    for template in template_directory:
        template_path = os.path.join(args.template_directory,
                                     template)
        template_name, template_data = load_template(logger, template_path)
        templates[template_name] = template_data

    for template_name, template_data in templates.items():
        apply_template(logger, es, args.overwrite_templates, template_name,
                       template_data)


if __name__ == '__main__':
    main()
