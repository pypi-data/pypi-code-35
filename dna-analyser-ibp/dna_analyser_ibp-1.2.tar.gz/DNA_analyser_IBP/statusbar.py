# statusbar.py
# !/usr/bin/env python3
"""
File with statusbar function used as indicator for callers
Available functions:
- status_bar: function implementing tqdm statusbar
"""

import time
from typing import Union

from tqdm import tqdm

from .callers.user_caller import User
from .callers.analyse_caller import Analyse
from .callers.g4hunter_caller import G4HunterAnalyse, g4_load_by_id
from .callers.p53_caller import P53Analyse, p53_load_by_id
from .callers.sequence_caller import SequenceModel, seq_load_by_id


def status_bar(user: User, obj: Union[SequenceModel, Analyse]) -> None:
    """
    Status bar function check upload status in interval 0 - 50 - 100 %.
    :param user: user for auth
    :param obj: object sequence or analyse => G4Hunter, P53
    """
    # tqdm status bar
    with tqdm(
        unit=" % uploaded" if isinstance(obj, SequenceModel) else " % processed",
        ascii=True,
        desc=f"Sequence {obj.name} uploading"
        if isinstance(obj, SequenceModel)
        else f"Analyse {obj.title} processing",
    ) as pbar:
        while True:
            pbar.update(50 - pbar.n)  # set 50 % when finished 100 %

            if isinstance(obj, SequenceModel):
                if obj.length is not None:  # that means if finnished
                    pbar.update(50)  # complete to to 100%
                    return None
                else:
                    obj = seq_load_by_id(user=user, id=obj.id)  # reload object

            if isinstance(obj, Analyse):
                if obj.finished is not None:  # that means analyse finnished
                    pbar.update(50)  # complete to to 100%
                    return None
                if isinstance(obj, G4HunterAnalyse):
                    obj = g4_load_by_id(user=user, id=obj.id)  # reload g4hunter object
                if isinstance(obj, P53Analyse):
                    obj = p53_load_by_id(user=user, id=obj.id)  # reload p53 object

            time.sleep(1)
