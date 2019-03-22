import os
import logging

import fiddler.cli_utils


class ImportCmd:

    def __init__(self, args):
        self.org = args.org
        self.api_endpoint = args.api_endpoint
        self.auth_key = args.auth_key

    def run(self):
        message = 'Not a dataset directory {}. Rerun this ' \
                  'command from a dataset directory'
        cwd = os.getcwd()
        dataset = cwd.split(os.sep)[-1]
        if not os.path.isfile('{}.yaml'.format(dataset)):
            logging.info(message.format(cwd))
            return

        path_items = cwd.split(os.sep)
        length = len(path_items)
        if length < 2:
            logging.info(message.format(cwd))
            return

        url = '{}/import_dataset/{}/{}'.format(
            self.api_endpoint,
            self.org,
            dataset
        )

        resp = fiddler.cli_utils.req_get(self.auth_key, url)
        for line in resp.iter_lines():
            # filter out keep-alive new lines
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)
        logging.info('Imported %s %s successfully', self.org, dataset)
        return resp
