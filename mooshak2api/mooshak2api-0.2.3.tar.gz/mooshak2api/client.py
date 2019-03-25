import requests

from mooshak2api.user import User


class Client:
    """
    A bundling of a mooshak2 endpoint, and a User. In most cases you should use mooshak2api.login rather than initiating
    this class yourself.

    You should add a User to this Object manually, via using self.user.
    Included are default headers that should be used for most JSON based messages.
    """
    endpoint = None
    user = None

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self, endpoint):
        self.endpoint = endpoint
        assert self.test()

    def headers_with_auth(self) -> dict:
        """
        Returns common headers with the JWT Header included. Ensure that self.user is a User Object, and that
        the user has been logged in with the .login() method.

        :return: returns a dict containing headers
        """
        try:
            return {**self.headers, "Authorization": f"Bearer {self.user.token}"}
        except AttributeError:
            raise Exception("You should ensure that this client has a user set, and that the user has been logged in!")

    def test(self):
        """
        Tests the connection.rst to the server

        :return: returns True if a connection.rst could be made
        """
        r = requests.get(self.endpoint)
        return r.json()["result"]["value"] == "Welcome to Mooshak 2.0 API"

    def refresh(self):
        """
        Refreshes this users token. Should be called every x seconds, in order to ensure that the user stays logged in
        """
        r = requests.post(f"{self.endpoint}auth/refresh/", headers=self.headers_with_auth())
        r.raise_for_status()


def login(endpoint, username, password, contest=None, admin=False):
    """
    Creates an authenticated client to interact with the Mooshak 2 API

    :param endpoint: The API Endpoint, ending in a slash. E.g,  https://mooshak2.dcc.fc.up.pt/mooshak-test/api/
    :param username: A username for the connection.rst, E.g. admin
    :param password: A password for the connection.rst, E.g. admin
    :param contest: The contest for the (non admin) user to interact with
    :param admin: If this is an admin account, and you want to administrate
    :return: A Client Object
    """
    if not admin and contest is None:
        raise Exception("You must specify a contest, or set admin to True")

    client = Client(endpoint)

    client_user = User(username, password, contest=contest, admin=admin)
    client_user.login(client)

    client.user = client_user
    return client
