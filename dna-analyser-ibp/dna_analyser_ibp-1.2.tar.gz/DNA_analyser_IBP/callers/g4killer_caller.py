# g4killer_caller.py
# !/user/bin/env python 3
"""Library with G4Killer object.
Available classes:
- G4KillerAnalyse: G4Killer analyse object
- G4KillerAnalyseFactory: G4Killer analyse factory
"""

import json
from typing import Union

import pandas as pd
import requests

from .analyse_caller import AnalyseFactory
from .user_caller import User


class G4KillerAnalyse:
    """G4Killer analyse object desctroi guanin quadruplex and change gscore"""

    def __init__(self, **kwargs):
        self.origin_score = kwargs.pop("originScore")
        self.target_threshold = kwargs.pop("targetThreshold")
        self.origin_sequence = kwargs.pop("originSequence")
        self.mutation_sequence = kwargs.pop("mutationSequence")
        self.mutation_score = kwargs.pop("mutationScore")

    def get_dataframe(self) -> pd.DataFrame:
        """
        Returns pandas dataframe for current object.
        :return: pandas dataframe
        """
        data_frame = pd.DataFrame().from_records(
            self.__dict__, columns=self.__dict__.keys(), index=[0]
        )
        return data_frame


class G4KillerAnalyseFactory(AnalyseFactory):
    """G4Killer factory used to generate analyse for given sequence string"""

    def create_analyse(
        self, user: User, origin_sequence: str, threshold: float
    ) -> Union[G4KillerAnalyse, Exception]:
        """
        G4killer analyse factory
        :param user: user for auth
        :param origin_sequence: origin sequence for killing procedure
        :param threshold: target threshold for new gscore
        :return: G4Killer object
        """

        # check range of parameters
        if 0 <= threshold <= 4:

            header = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "Authorization": user.jwt,
            }

            data = json.dumps({"sequence": origin_sequence, "threshold": threshold})

            response = requests.post(
                f"{user.server}/analyse/g4killer", headers=header, data=data
            )

            if response.status_code == 201:
                data = response.json()
                if data:
                    return G4KillerAnalyse(**data)
                else:
                    raise ValueError(response.status_code, "Server returend no data")
            else:
                raise ConnectionError(response.status_code, "Server error")
        else:
            raise ValueError("Value threshold out of range")
