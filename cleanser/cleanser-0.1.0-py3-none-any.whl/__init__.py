"""Cleanser"""
from cleanser.core.generic import Generic
from cleanser.core.reddit import Reddit


class Cleanser(Generic, Reddit):
    """Class does stuff"""

    def __init__(self, text):
        super().__init__()
        self.text = text
