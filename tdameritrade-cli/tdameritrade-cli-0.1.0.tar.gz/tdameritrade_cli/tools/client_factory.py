import json
from json.decoder import JSONDecodeError

import click
from tdameritrade_client.client import TDClient


class ClientFactory(object):
    def __init__(self, json_config: str = None, acct_number: int = None, oauth_user_id: str = None,
                 redirect_uri: str = None):
        """
        A factory of TDClient objects. Must pass either a valid json_config or an (acct_number, oauth_user_id) pair.
        If not supplied, redirect_uri defaults to http://127.0.0.1:8080.

        Args:
            json_config: A json object with acct_number, oauth_user_id, and redirect_uri keys.
                         May also have token_path.
            acct_number: A TDAmeritrade account number.
            oauth_user_id: The TDDeveloper app OAuth user ID.
            redirect_uri: The TDDeveloper app redirect URI.

        Raises:
            click.Abort: If no valid configuration is passed.

        """

        if json_config is None and [acct_number, oauth_user_id] == [None, None]:
            click.echo('Must either pass a json_config or, at minimum, ' \
                       'an acct_number and an oauth_user_id. See tda-cli --help.')
            raise click.Abort()
        self.json = json_config
        self.acct_number = acct_number
        self.oauth_user_id = oauth_user_id
        self.redirect_uri = redirect_uri

    def from_json(self):
        """
        Create a TDClient from a json_config

        Returns:
            An authenticated TDClient.

        Raises:
            IsADirectoryError: Bad path to json_config
            JSONDecodeError: Bad path to json_config

        """

        try:
            with open(self.json) as f:
                config = json.load(f)
        except IsADirectoryError:
            raise IsADirectoryError('Path to json_config does not lead to a file!')
        except JSONDecodeError:
            raise ValueError('Path to json_config does not lead to a valid json file!')

        client = TDClient(**config)
        client.run_auth()
        return client

    def from_config(self):
        """
        Create a TDClient from passed parameters

        Returns:
            An authenticated TDClient.

        """

        client = TDClient(acct_number=self.acct_number,
                          oauth_user_id=self.oauth_user_id,
                          redirect_uri=self.redirect_uri)
        client.run_auth()
        return client
