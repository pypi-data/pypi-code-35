from typing import Union, Iterable

import requests
from mooshak2api.contests import get as get_contest
from mooshak2api.client import Client
from mooshak2api.contests import Contest
from mooshak2api.evaluation import Evaluation
from mooshak2api.factory import GenericObject


class Problem(GenericObject):
    """
    A problem of a Contest.
     It must contain a Contest ID, as the REST API does not allow accessing problems directly

    """
    def __init__(self, contest_id):
        super(Problem, self).__init__()
        self.contest_id = contest_id
    contest_id = None

    def update(self, connection: Client):
        r = requests.put(
            f"{connection.endpoint}data/contests/{self.contest_id}/problems/{self.id}",
            headers=connection.headers_with_auth(),
            json=self.as_json()
        )
        return r

    def delete(self, connection: Client):
        r = requests.delete(
            f"{connection.endpoint}data/contests/{self.contest_id}/problems/{self.id}",
            headers=connection.headers_with_auth()
        )
        return r

    def get_contest(self, connection: Client):
        return get_contest(connection, self.contest_id)

    def evaluate(self, connection: Client, problem_code):
        files = {"program": problem_code}
        headers = connection.headers_with_auth().copy()
        headers.pop("Content-Type")
        headers.pop("Accept")
        r = requests.post(
            f"{connection.endpoint}data/contests/{self.contest_id}/problems/{self.id}/evaluate",
            headers=headers,
            files=files
        )
        if int(r.status_code) == 500:
            raise Exception(r.json()["message"])
        return Evaluation(self.contest_id, self.id).load_from_dict(r.json())


def get(connection: Client, contest: Union[Contest, int], problem_id: int) -> Problem:
    if type(contest) is Contest:
        contest = contest.id
    r = requests.get(f"{connection.endpoint}data/contests/{contest}/problems/{problem_id}",
                     headers=connection.headers_with_auth())
    r.raise_for_status()
    problem = Problem(contest).load_from_dict(r.json())
    return problem


def get_all(connection: Client, contest: Union[Contest, int]) -> Iterable[Problem]:
    if type(contest) is Contest:
        contest = contest.id
    r = requests.get(
        f"{connection.endpoint}data/contests/{contest}/problems/",
        headers=connection.headers_with_auth())
    results = []
    for c in r.json():
        results.append(Problem(contest).load_from_dict(c))
    return results

