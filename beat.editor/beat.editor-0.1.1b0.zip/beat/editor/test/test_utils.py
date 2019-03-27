#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.cmdline module of the BEAT platform.          #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################

# test the utils.py file
# (mostly python file generation via jinja2 templates)

import nose.tools
import os

from .. import utils

def test_generate_empty_database():
    empty_db = """# You may import any python packages that will be available in the environment you will run this database in
# Environments can change based on the experiment's settings
from beat.backend.python.database import View

class View(View):
    # build the data for your view
    # split the raw data into (homogenous) bits and return a keyed iterable
    # (something with `.keys()` available to it, like a dict)
    # the key names must be the same as the output names for sets that use this view
    #    root_folder: the path to the root folder of the database's files (not always applicable)
    #    parameters: parameters passed to the view, defined in the metadata
    def index(self, root_folder, parameters):
        pass

    # returns a value at a specific index in the iterable for this view
    #   output: the specific output value requested
    #   index: the current index of the iterable
    def get(self, output, index):
        # to get the current object referenced by the given index:
        #       obj = self.objs[index]
        # note that this object is a named tuple, with fields equivalent to your keys from
        # the objects returned from the index function
        pass
"""
    str = utils.generate_database()
    nose.tools.eq_(str, empty_db)

def test_generate_empty_algorithm():
    empty_alg = """# You may import any python packages that will be available in the environment you will run this algorithm in
# Environments can change based on the experiment's settings

class Algorithm:
    # initialise fields to store cross-input data (e.g. machines, aggregations, etc.)
    def __init__(self):
        pass

    # this will be called each time the sync'd input has more data available to be processed
    def process(self, inputs, outputs):
        # Groups available:

        # to check if there is more data waiting in the inputs
        # (if it is False, you have processed all the inputs and this "process" function won't be called again):
        #       if inputs.hasMoreData():

        # to check if a specific input is done:
        #       if inputs["input1"].isDataUnitDone():

        # to manually fetch the next input of a specific input
        # (e.g. the block is not sync'd to the input but you want the input immediately)
        #       inputs['input1'].next()
        # you can then access that input value as normal:
        #       self.val1 = inputs['input1'].data

        # to get the data for an input (note that the value will be of the type specified in the metadata!):
        #       data_value = inputs['input1'].data

        # to write to an output:
        #       outputs['output1'].write({
        #           'output_field_1': 1,
        #           'output_field_2': 'output'
        #       })

        # always return True, it signals BEAT to continue processing
        return True"""

    alg = { 'name': 'user/alg/1', 'contents': { 'splittable': True, 'groups': [], 'uses': {} }}
    str = utils.generate_algorithm(alg['contents'])
    nose.tools.eq_(str, empty_alg)

def test_generate_empty_library():
    empty_lib = """# You may import any python packages that will be available in the environment you will run this library in
# Environments can change based on the experiment's settings
"""

    str = utils.generate_library()
    nose.tools.eq_(str, empty_lib)
