# -*- coding: utf-8 -*-
"""
对话策略模块
"""

from typing import List
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from ..common.system_action import SystemAction
from ..common.dialog_state import DialogState


class DialogPolicy(object):

    def __init__(self):
        self.clf = None

    def forward(self,
                history: List[DialogState]):
        x = np.array([
            s.vec
            for s in history
        ]).flatten()
        pred = self.clf.predict(np.array([x])).flatten()
        pred = pred.argmax()
        system_action = SystemAction(history[-1].index_sys_intent[pred])
        return system_action

    def fit(self, x, y):
        clf = RandomForestClassifier(n_estimators=100)
        clf.fit(x, y)
        self.clf = clf
