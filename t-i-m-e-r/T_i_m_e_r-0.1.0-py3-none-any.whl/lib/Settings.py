import pickle
import os

from .TreeDB import TreeDB


class Settings(TreeDB):
    def __init__(self, filename):
        TreeDB.__init__(self)

        self._filename = filename
        self._tosave = []

    def load(self):
        if not os.path.exists(self._filename):
            return

        with open(self._filename, 'rb') as ifs:
            self._d = pickle.load(ifs)

    def save(self):
        for key, func in self._tosave:
            self[key] = func()

        os.makedirs(os.path.dirname(self._filename) or '.', exist_ok=True)
        with open(self._filename, 'wb') as ofs:
            pickle.dump(self._d, ofs)

    def tosave(self, key, func):
        self._tosave.append((key, func))
