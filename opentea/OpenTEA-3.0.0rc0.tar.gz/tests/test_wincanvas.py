# pylint: disable=missing-docstring
import shutil
import os

from os.path import join
from textwrap import dedent

import pytest

from .context import opentea, Project, viewer3d_case_utilities

import numpy as np


class TestWinCanvas(Project):
    @classmethod
    def setup_class(cls):
        super(TestWinCanvas, cls).setup_class()
