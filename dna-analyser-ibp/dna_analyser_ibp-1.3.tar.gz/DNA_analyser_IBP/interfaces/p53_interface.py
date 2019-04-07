# p53_interface.py
# !/usr/bin/env python3
"""Library with P53 interface object
Available classes:
P53 - interface for interaction with p53 api
"""

import time
import pandas as pd

from ..statusbar import status_bar
from .api_interface import ApiInterface

from typing import List, Union
from ..callers.user_caller import User

from ..callers.p53_caller import (
    P53AnalyseFactory,
    p53_delete_analyse,
    p53_load_all,
    p53_load_by_id,
)


class P53(ApiInterface):
    """Api interface for p53 caller"""

    def __init__(self, user: User):
        self.user = user

    def load_all(self, filter_tag: List[str] = None) -> pd.DataFrame:
        """
        Return all or tag filtered p53 analyse dataframe.
        :param filter_tag: tags for filtering result dataframe
        :return: pandas dataframe with p53 analyses
        """
        p53 = [p53 for p53 in p53_load_all(user=self.user, filter_tag=filter_tag)]
        data = pd.concat([p.get_dataframe() for p in p53], ignore_index=True)
        return data

    def load_by_id(self, id: str) -> pd.DataFrame:
        """
        Return p53 dataframe by given id.
        :param id: id for getting result dataframe
        :return: pandas dataframe with p53 analyse
        """
        p53 = p53_load_by_id(user=self.user, id=id)
        return p53.get_dataframe()

    def analyse_creator(
        self, sequence: Union[pd.DataFrame, pd.Series], tags: List[str], threshold: int
    ):
        """
        Send request with sequence and create p53 analyse.
        :param sequence: sequence to analyse
        :param tags: list of tags for created analyse
        :param threshold: threshold for p53 analyse
        """
        # start p53 analyse factory
        if isinstance(sequence, pd.DataFrame):
            for _, row in sequence.iterrows():
                p53_fact = P53AnalyseFactory(
                    user=self.user, id=row["id"], tags=tags, threshold=threshold
                )
                status_bar(user=self.user, obj=p53_fact.analyse)
        else:
            p53_fact = P53AnalyseFactory(
                user=self.user, id=sequence["id"], tags=tags, threshold=threshold
            )
            status_bar(user=self.user, obj=p53_fact.analyse)

    def delete(self, p53_pandas: Union[pd.DataFrame, pd.Series]):
        """
        Delete given p53 analyse or p53 analyses.
        :param p53_pandas: dataframe with multiple p53 analyses or series with one
        """
        if isinstance(p53_pandas, pd.DataFrame):
            # delete each p53 in pandas dataframe
            for _, row in p53_pandas.iterrows():
                _id = row["id"]
                if p53_delete_analyse(user=self.user, id=_id):
                    print(f"P53 {_id} was deleted")
                    time.sleep(1)
                else:
                    print("P53 cannot be deleted")
        else:
            _id = p53_pandas["id"]
            if p53_delete_analyse(user=self.user, id=_id):
                print(f"P53 {id} was deleted")
            else:
                print("P53 cannot be deleted")
