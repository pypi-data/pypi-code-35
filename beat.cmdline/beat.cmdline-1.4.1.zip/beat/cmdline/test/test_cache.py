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


# Basic tests for the command line beat program: cache

import os
import click
from click.testing import CliRunner
import nose.tools

from . import prefix, tmp_prefix, temp_cwd
from .utils import index_experiment_dbs

from beat.cmdline.scripts import main_cli

from beat.core.test.utils import cleanup, slow


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''

  use_prefix = kwargs.get('prefix', prefix)

  runner = CliRunner()
  with runner.isolated_filesystem():
    result = runner.invoke(
        main_cli.main,
        ['--test-mode', '--prefix', use_prefix, '--cache', tmp_prefix] +
        list(args)
    )
  return result.exit_code, result.output


def setup_module():
  experiment_name = 'user/user/double_triangle/1/double_triangle'

  index_experiment_dbs(experiment_name)

  call('experiments', 'run', experiment_name)

def teardown_module():
  cleanup()


@slow
def test_cache_info():
  assert len(os.listdir(tmp_prefix)) != 0
  ex_code, out = call('cache', 'info')
  nose.tools.eq_(ex_code, 0, out)
  ex_code, out = call('cache', 'info', '--sizes')
  nose.tools.eq_(ex_code, 0, out)
  ex_code, out = call('cache', '--start', 0, 'info')
  nose.tools.eq_(ex_code, 0, out)


@slow
def test_cache_view():
  assert len(os.listdir(tmp_prefix)) != 0
  ex_code, out = call('cache', 'view')
  nose.tools.eq_(ex_code, 0, out)
  ex_code, out = call('cache', '--start', 0, 'view')
  nose.tools.eq_(ex_code, 0, out)


@slow
def test_cache_clear():
  assert len(os.listdir(tmp_prefix)) != 0
  ex_code, out = call('cache', 'clear')
  nose.tools.eq_(ex_code, 0, out)
  nose.tools.eq_(len(os.listdir(tmp_prefix)), 0)
