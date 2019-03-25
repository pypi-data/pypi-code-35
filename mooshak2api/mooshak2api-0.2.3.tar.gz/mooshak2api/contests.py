from typing import Iterable

import requests

from mooshak2api.client import Client
from mooshak2api.factory import GenericObject


class Contest(GenericObject):
    """
    A Mooshak2 Contest. The only required property that is required is an ID


    """

    def update(self, connection):
        """
        Updates a Contest
        :param connection: the Client to connect with
        :return: returns a request - with status 201 if successful
        """
        r = requests.put(
            f"{connection.endpoint}data/contests/{self.id}/",
            headers=connection.headers_with_auth(),
            json=self.as_json()
        )
        return r

    def delete(self, connection):
        """
        Deletes a Contest
        :param connection: the Client to connect with
        :return: returns a request - with status 201 if successful
        """
        r = requests.delete(
            f"{connection.endpoint}data/contests/{self.id}/",
            headers=connection.headers_with_auth()
        )
        return r

    def create(self, connection):
        """
        Creates a Contest

        You should ensure that the contest has ID set, and that any properties that you want to add are in
        self.property_names
        :param connection: the Client to connect with
        :return: returns a request - with status 201 if successful
        """
        r = requests.post(
            f"{connection.endpoint}data/contests/",
            headers=connection.headers_with_auth(),
            json=self.as_json()
        )
        return r


def get(connection: Client, contest_id: str) -> Contest:
    """
    Gets a single Contest
    :param connection: Client to connect to
    :param contest_id: the ID of the contest. e.g. ToPAS14
    :return: returns a Contest
    """
    r = requests.get(f"{connection.endpoint}data/contests/{contest_id}/", headers=connection.headers_with_auth())
    return Contest().load_from_dict(r.json())


def get_all(connection: Client) -> Iterable[Contest]:
    r = requests.get(f"{connection.endpoint}data/contests/", headers=connection.headers_with_auth())
    results = []
    for c in r.json():
        results.append(Contest().load_from_dict(c))
    return results

