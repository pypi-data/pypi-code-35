#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


# Docker based tests for algorithms and analyzers

import os
import json
import shutil
import pkg_resources
from beat.core.test.utils import slow, cleanup, skipif

import nose.tools

from beat.backend.python.hash import hashDataset
from beat.backend.python.hash import toPath
from beat.core.database import Database

from .test_algorithms import call as call_algo
from .test_experiments import call as call_xp
from . import prefix, tmp_prefix


instructions_dir = pkg_resources.resource_filename(__name__, 'instructions')


def index_db_from_instructions(input_field):
  database = Database(prefix, input_field['database'])
  view = database.view(input_field['protocol'], input_field['set'])
  filename = toPath(hashDataset(input_field['database'],
                                input_field['protocol'],
                                input_field['set']),
                                suffix='.db')
  view.index(os.path.join(tmp_prefix, filename))


@slow
@nose.tools.with_setup(teardown=cleanup)
def test_execute_algorithm_using_database():
  instructions = os.path.join(instructions_dir, 'algo_using_database.json')
  with open(instructions) as instruction_file:
    instructions_data = json.load(instruction_file)
  input_field = instructions_data['inputs']['in']
  index_db_from_instructions(input_field)

  exit_code, outputs = call_algo('execute', instructions, cache=tmp_prefix)
  nose.tools.eq_(exit_code, 0, msg=outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
def test_execute_algorithm_using_cached_files():
  cache_dir = os.path.join(tmp_prefix, 'ab', 'cd', 'ef')

  os.makedirs(cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data.checksum'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index.checksum'), cache_dir)

  instructions = os.path.join(instructions_dir, 'algo_using_cached_files.json')

  exit_code, outputs = call_algo('execute', instructions, cache=tmp_prefix)
  nose.tools.eq_(exit_code, 0, msg=outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
def test_execute_algorithm_using_database_and_cached_files():
  cache_dir = os.path.join(tmp_prefix, 'ab', 'cd', 'ef')

  os.makedirs(cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data.checksum'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index.checksum'), cache_dir)

  instructions = os.path.join(instructions_dir, 'algo_using_database_and_cached_files.json')

  with open(instructions) as instruction_file:
    instructions_data = json.load(instruction_file)
  input_field = instructions_data['inputs']['in1']
  index_db_from_instructions(input_field)

  exit_code, outputs = call_algo('execute', instructions, cache=tmp_prefix)
  nose.tools.eq_(exit_code, 0, msg=outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
def test_execute_analyzer():
  cache_dir = os.path.join(tmp_prefix, 'ab', 'cd', 'ef')

  os.makedirs(cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.data.checksum'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index'), cache_dir)
  shutil.copy(os.path.join(instructions_dir, '0123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.0.9.index.checksum'), cache_dir)

  instructions = os.path.join(instructions_dir, 'analyzer.json')

  exit_code, outputs = call_algo('execute', instructions, cache=tmp_prefix)
  nose.tools.eq_(exit_code, 0, msg=outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
def test_run_single_error_1_docker():
  # When running on docker, the module is loaded in the docker
  # container and the local process will return '1'.
  obj = 'user/user/single/1/single_error'
  nose.tools.eq_(call_xp('run', obj, '--docker', cache=tmp_prefix), 1)


@slow
@nose.tools.with_setup(teardown=cleanup)
def test_run_single_error_twice_docker():
  # This one makes sure our output reset is working properly. Both tries should
  # give out the same error.
  obj = 'user/user/single/1/single_error'
  nose.tools.eq_(call_xp('run', obj, '--docker', cache=tmp_prefix), 1)
  nose.tools.eq_(call_xp('run', obj, '--docker', cache=tmp_prefix), 1)
