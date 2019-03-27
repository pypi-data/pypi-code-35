#!/usr/bin/env python
# coding: utf-8
#
# Usage: 
# Author: xuwenqiang0563@163.com

import os
import sys
sys.path = [os.path.dirname(os.path.realpath(__file__)) + "/so/"] + sys.path

import cythonsp
from cythonsp import TaskMode, SegmentorFactory
