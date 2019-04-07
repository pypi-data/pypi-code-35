# p53_caller.py
# !/usr/bin/env python3
"""Library with P53 object.
Available classes:
- P53Analyse: P53 analyse object
- P53AnalyseFactory: P53 analyse factory
Available functions:
- p53_delete_analyse: delete p53 analyse
- p53_load_by_id:  return p53 analyse by id
- p53_load_all: return all or filtered p53 analyses
"""

import json
from typing import Generator, List, Union
from .user_caller import User

import pandas as pd
import requests

from .analyse_caller import AnalyseFactory, Analyse
from ..utils import generate_dataframe


class P53Analyse(Analyse):
    """P53 analyse object finds p53 protein in DNA/RNA sequence."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_count = kwargs.pop("resultCount")
        self.threshold = kwargs.pop("threshold")

    def __str__(self):
        return f"P53 {self.id} {self.title}"

    def __repr__(self):
        return f"<P53 {self.id} {self.title}>"


class P53AnalyseFactory(AnalyseFactory):
    """P53 factory used for generating analyse for given sequence."""

    def create_analyse(
        self, user: User, id: str, tags: List[str], threshold: int
    ) -> Union[P53Analyse, Exception]:
        """
        P53 analyse factory.
        :param user: user for auth
        :param id: sequence id to create p53 analyse
        :param tags: tags for future filtering
        :param threshold: threshold for p53 algorithm
        :return: P53 object
        """

        header = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": user.jwt,
        }

        data = json.dumps({"sequences": [id], "tags": tags, "threshold": threshold})

        response = requests.post(
            f"{user.server}/analyse/p53predictor", headers=header, data=data
        )

        if response.status_code == 201:
            data = response.json()["items"]
            if data:
                return P53Analyse(**data[0])
            else:
                raise ValueError(response.status_code, "Server returned no data")
        else:
            raise ConnectionError(response.status_code, "Server error")


def p53_delete_analyse(user: User, id: str) -> bool:
    """
    Delete finished analyse for given object id.
    :param user: user for auth
    :param id: p53 analyse id to delete
    :return: True if delete success and False if not
    """
    header = {
        "Content-type": "application/json",
        "Accept": "*/*",
        "Authorization": user.jwt,
    }
    response = requests.delete(
        f"{user.server}/analyse/p53predictor/{id}", headers=header
    )

    if response.status_code == 204:
        return True
    return False


def p53_load_by_id(user: User, id: str) -> Union[P53Analyse, Exception]:
    """
    Load p53 analyse for current user with current p53 id.
    :param user: user for auth
    :param id: p53 id
    :return: found p53 analyse
    """

    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }

    response = requests.get(f"{user.server}/analyse/p53predictor/{id}", headers=header)

    if response.status_code == 200:
        data = response.json()["payload"]
        if data:
            return P53Analyse(**data)
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


def p53_load_all(
    user: User, filter_tag: List[str]
) -> Union[Generator[P53Analyse, None, None], Exception]:
    """
        List all p53 analyses for current user with all or filtered analyses.
        :param user: user for auth
        :param filter_tag: tag for filtering final dataframe
        :return: all or filtered yield p53 analyses
        """

    # FIXME: filter_tag not implemented in API have to FIX in future

    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }

    params = {"requestForAll": "true", "pageSize": "ALL"}

    response = requests.get(
        f"{user.server}/analyse/p53predictor", headers=header, params=params
    )

    if response.status_code == 200:
        data = response.json()["items"]
        if data:
            for rec in data:
                # yield P53 object from list
                yield P53Analyse(**rec)
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


def p53_load_result(user: User, id: str) -> Union[Exception, pd.DataFrame]:
    """
    Load p53 analysis result as pandas dataframe.
    :param user: user for auth
    :param id: p53 analysis
    :return: pandas dataframe with p53 results
    """

    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": user.jwt,
    }

    params = {"order": "ASC", "requestForAll": "true", "pageSize": "ALL"}

    response = requests.get(
        f"{user.server}/analyse/p53predictor/{id}/result", headers=header, params=params
    )

    if response.status_code == 200:
        data = response.json()["items"]
        if data:
            return generate_dataframe(res=data)
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")


def p53_export_csv(user: User, id: str) -> Union[Exception, str]:
    """
    Download csv output as raw text.
    :param user: user for auth
    :param id: p53 analysis
    :return: raw text output in csv format
    """

    header = {"Accept": "text/plain", "Authorization": user.jwt}

    response = requests.get(
        f"{user.server}/analyse/p53predictor/{id}/export.csv", headers=header
    )

    if response.status_code == 200:
        csv_str = response.text
        if csv_str:
            return csv_str
        else:
            raise ValueError(response.status_code, "Server returned no data")
    else:
        raise ConnectionError(response.status_code, "Server error")
