import os
import pandas as pd
import numpy as np
from scipy.io import wavfile
from keras.preprocessing.image import load_img


class Foundation:

    """Foundation for construction"""

    def __init__(self):
        pass  # Not Finished


class TextObj:

    """Cortecx Text Object"""

    def __init__(self, text: str):
        self.text = str(text)

        instance_count = 0
        if instance_count == 0:
            self.original_text = self.text
        else:
            self.original_text = self.original_text

    def apply(self, cls):
        self.text = cls.process(self.text)

    def wipe(self):
        self.text = None


class DataObj:

    """Cortecx Data Object"""

    def __init__(self, data=None, file_path=None):
        if file_path is not None:
            if data is not None:
                raise ValueError('data or file_path cannot both have values')

        if file_path is None:
            if data is None:
                raise ValueError('data and file_path can not both be None')

        self.file_path = file_path
        self.data = data

    def apply(self, cls):
        self.data = cls.process(self.data)

    def wipe(self):
        self.data = None

    def load_csv(self, columns=None, delimiter=','):
        self.data = pd.read_csv(self.file_path, delimiter=delimiter, names=columns)

    def load_tsv(self, columns=None, delimiter='\t'):
        self.data = pd.read_csv(self.file_path, delimiter=delimiter, names=columns)

    def load_json(self):
        self.data = pd.read_json(self.file_path)

    def load_img(self, file_path):
        self.data = load_img(file_path)

    def load_audio(self, file_path):
        self.data = wavfile.read(file_path)
