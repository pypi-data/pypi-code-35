# g4hunter_caller.py
# !/usr/bin/env python3
"""Library with G4hunter object.
Available classes:
- G4HunterAnalyse: G4hunter analyse object
- G4HunterAnalyseFactory: G4hunter analyse factory
Available functions:
- g4_delete_analyse: delete g4hunter analyse
- g4_load_by_id:  return g4hunter analyse by id
- g4_load_all: return all or filtered g4hunter analyses
- g4_load_result: load analyse data as pandas dataframe
- g4_export_csv: export g4hunter result as string in csv format
- g4_load_heatmap: load heatmap data as list of dicts
"""

import json
from typing import Generator, List, Union
from .user_caller import User

import pandas as pd
import requests

from .analyse_caller import AnalyseFactory, Analyse
from ..utils import generate_dataframe


class G4HunterAnalyse(Analyse):
    """G4Hunter analyse object finds guanine quadruplex in DNA/RNA sequence."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_count = kwargs.pop("resultCount")
        self.window_size = kwargs.pop("windowSize")
        self.threshold = kwargs.pop("threshold")
        self.frequency = kwargs.pop("frequency")

    def __str__(self):
        return f"G4Hunter {self.id} {self.title}"

    def __repr__(self):
        return f"<G4Hunter {self.id} {self.title}>"


class G4HunterAnalyseFactory(AnalyseFactory):
    """G4Hunter factory used for generating analyse for given sequence."""

    def create_analyse(
        self, user: User, id: str, tags: List[str], threshold: float, window_size: int
    ) -> Union[G4HunterAnalyse, Exception]:
        """
        G4hunter analyse factory
        :param user: user for auth
        :param id: sequence id to create g4hunter analyse
        :param tags: tags for future filtering
        :param threshold: threshold for g4hunter algorithm recommended 1.4
        :param window_size: window size for g4hunter algorithm recommended 25
        :return: G4hunter object
        """

        if (
            0.1 <= threshold <= 4 and 10 <= window_size <= 100
        ):  # check range of parameters
            header = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "Authorization": user.jwt,
            }

            data = json.dumps(
                {
                    "sequences": [id],
                    "tags": tags,
                    "threshold": threshold,
                    "windowSize": window_size,
                }
            )

            response = requests.post(
                f"{user.server}/analyse/g4hunter", headers=header, data=data
            )

            if response.status_code == 201:
                data = response.json()["items"]
                if data:
                    return G4HunterAnalyse(**data[0])
                else:
                    raise ValueError(response.status_code, "Server returned no data")
            else:
                raise ConnectionError(response.status_code, "Server error")
        else:
            raise ValueError("Value window size or threshold out of range.")


def g4_delete_analyse(user: User, id: str) -> bool:
    """
    Delete finished analyse for given object id.
    :param user: user for auth
    :param id: g4hunter analyse id to delete
    :return: True if delete success and False if not
    """
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": user.jwt,
    }
    response = requests.delete(f"{user.server}/analyse/g4hunter/{id}", headers=header)

    if response.status_code == 204:
        return True
    return False


def g4_load_by_id(user: User, id: str) -> Union[G4HunterAnalyse, Exception]:
    """
    List one g4hunter analyse for current user with current g4hunter id.
    :param user: user for auth
    :param id: g4hunter analyse id
    :return: found g4hunter analyse
    """
    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }

    response = requests.get(f"{user.server}/analyse/g4hunter/{id}", headers=header)

    if response.status_code == 200:
        data = response.json()["payload"]
        if data:
            return G4HunterAnalyse(**data)
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


def g4_load_all(
    user: User, filter_tag: List[str]
) -> Union[Generator[G4HunterAnalyse, None, None], Exception]:
    """
    List all g4hunter analyses for current user with all or filtered analyses.
    :param user: user for auth
    :param filter_tag: tag for filtering final dataframe
    :return: all or filtered yield g4hunter analyses
    """
    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }

    params = {
        "order": "ASC",
        "requestForAll": "true",
        "pageSize": "ALL",
        "tags": filter_tag if filter_tag else None,
    }

    response = requests.get(
        f"{user.server}/analyse/g4hunter", headers=header, params=params
    )

    if response.status_code == 200:
        data = response.json()["items"]
        if data:
            for rec in data:
                # yield G4hunter object from list
                yield G4HunterAnalyse(**rec)
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


def g4_load_result(user: User, id: str) -> Union[Exception, pd.DataFrame]:
    """
    Loads g4hunter analysis result as pandas dataframe.
    :param user: user for auth
    :param id: g4hunter analyse id
    :return: pandas dataframe with g4hunter results
    """

    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }

    params = {"order": "ASC", "requestForAll": "true", "pageSize": "ALL"}

    response = requests.get(
        f"{user.server}/analyse/g4hunter/{id}/quadruplex", headers=header, params=params
    )

    if response.status_code == 200:
        data = response.json()["items"]
        if data:
            return generate_dataframe(res=data)
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


def g4_export_csv(user: User, id: str, aggregate: bool = True) -> Union[Exception, str]:
    """
    Download csv output as raw text.
    :param user: user for auth
    :param id: g4hunter analyse id
    :param aggregate: true for aggregate form, false for not
    :return: raw text output in csv format
    """

    header = {"Accept": "text/plain", "Authorization": user.jwt}
    params = {"aggregate": "true" if aggregate else "false"}

    response = requests.get(
        f"{user.server}/analyse/g4hunter/{id}/quadruplex.csv",
        headers=header,
        params=params,
    )

    if response.status_code == 200:
        csv_str = response.text
        if csv_str:
            return csv_str
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


def g4_load_heatmap(
    user: User, id: str, segment_count: int
) -> Union[Exception, pd.DataFrame]:
    """
    Download heatmap data for analyse.
    :param user: user for auth
    :param id: g4hunter analyse id
    :param segment_count: number of segments
    :return: list with coverage, count data
    """

    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }
    params = {"segments": segment_count}

    response = requests.get(
        f"{user.server}/analyse/g4hunter/{id}/heatmap", headers=header, params=params
    )

    if response.status_code == 200:
        data = response.json()["data"]
        if data:
            return pd.DataFrame(data=data)
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")
