import requests
import datetime


class User:

    token = None
    last_refresh = None

    def __init__(self, username, password, contest=None, admin=False):
        self.username = username
        self.password = password
        self.admin = admin
        try:
            self.contest = contest.id
        except AttributeError:
            self.contest = contest

    def login(self, connection):
        json = {
            "username": self.username,
            "password": self.password,
        }
        if not self.admin:
            json.update({"contest": self.contest})

        r = requests.post(f"{connection.endpoint}auth/login/", json=json, headers=connection.headers)

        try:
            self.token = r.json()["token"]
            self.last_refresh = datetime.datetime.now()
        except KeyError:
            raise Exception(f"Unable to login - {r.text}")
