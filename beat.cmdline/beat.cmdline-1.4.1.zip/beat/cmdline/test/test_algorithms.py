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


# Basic tests for the command line beat program: algorithms

import nose.tools
import os
import click
from click.testing import CliRunner
import shutil
import json

from beat.core.test.utils import slow, cleanup, skipif
from beat.core.algorithm import Storage
from beat.cmdline.scripts import main_cli

from .. import common

from . import platform, disconnected, prefix, tmp_prefix, user, token, temp_cwd


def setup():
  """Create default dataformat for algorithm prototype loading"""

  from .test_dataformats import test_create as df_test_create
  from .test_dataformats import call as df_call
  obj = 'user/integers/1'

  nose.tools.eq_(df_call('create', obj, prefix=tmp_prefix), 0)
  if not disconnected:
    nose.tools.eq_(df_call('push', obj, prefix=tmp_prefix), 0)


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''

  use_prefix = kwargs.get('prefix', prefix)
  use_platform = kwargs.get('platform', platform)
  use_cache = kwargs.get('cache', 'cache')

  runner = CliRunner()
  with runner.isolated_filesystem():
    result = runner.invoke(
        main_cli.main,
        ['--platform', use_platform, '--user', user, '--token', token,
         '--prefix', use_prefix, '--cache', use_cache, '--test-mode',
         'algorithms'] + list(args),
         catch_exceptions=False
    )
    return result.exit_code, result.output


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_remote_list():
  exit_code, outputs = call('list', '--remote')
  nose.tools.eq_(exit_code, 0, msg=outputs)


@nose.tools.with_setup(teardown=cleanup)
def test_local_list():
  exit_code, outputs = call('list')
  nose.tools.eq_(exit_code, 0, outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one():
  obj = 'user/integers_add/1'
  exit_code, outputs = call('pull', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  s = Storage(tmp_prefix, obj)
  assert s.exists()


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_all():
  exit_code, outputs = call('pull', prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_diff():
  obj = 'user/integers_add/1'
  exit_code, outputs = call('pull', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)

  # quickly modify the user algorithm by emptying it
  storage = Storage(tmp_prefix, obj)
  storage.code.save('class Algorithm:\n  pass')

  exit_code, outputs = call('diff', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_status():
  test_diff()
  test_pull_one()
  exit_code, outputs = call('status', prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)


def test_check_valid():
  obj = 'legacy/valid_algorithm/1'
  exit_code, outputs = call('check', obj)
  nose.tools.eq_(exit_code, 0, outputs)


def test_check_invalid():
  obj = 'legacy/no_inputs_declarations/1'
  exit_code, outputs = call('check', obj)
  nose.tools.eq_(exit_code, 1, outputs)


@nose.tools.with_setup(setup=setup, teardown=cleanup)
def test_create(obj=None):
  obj = obj or 'legacy/algorithm/1'
  exit_code, outputs = call('create', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  s = Storage(tmp_prefix, obj)
  assert s.exists()
  return s


@nose.tools.with_setup(setup=setup, teardown=cleanup)
def test_new_version():
  obj = 'legacy/algorithm/1'
  test_create(obj)
  obj2 = 'legacy/algorithm/2'
  exit_code, outputs = call('version', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  s = Storage(tmp_prefix, obj2)
  assert s.exists()

  # check version status
  with common.Selector(tmp_prefix) as selector:
    assert selector.version_of('algorithm', obj2) == obj


@nose.tools.with_setup(setup=setup, teardown=cleanup)
def test_fork():
  obj = 'legacy/algorithm/1'
  test_create(obj)
  obj2 = 'legacy/different/1'
  exit_code, outputs = call('fork', obj, obj2, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  s = Storage(tmp_prefix, obj2)
  assert s.exists()

  # check fork status
  with common.Selector(tmp_prefix) as selector:
    assert selector.forked_from('algorithm', obj2) == obj


@nose.tools.with_setup(setup=setup, teardown=cleanup)
def test_delete_local():
  obj = 'legacy/algorithm/1'
  storage = test_create(obj)

  # quickly make sure it exists
  storage = Storage(tmp_prefix, obj)
  assert storage.exists()

  exit_code, outputs = call('rm', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  assert not storage.exists()


@nose.tools.with_setup(setup=setup, teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_push_and_delete():
  obj = 'user/newobject/1'
  test_create(obj)

  # now push the new object and then delete it remotely
  exit_code, outputs = call('push', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
  exit_code, outputs = call('rm', '--remote', obj, prefix=tmp_prefix)
  nose.tools.eq_(exit_code, 0, outputs)
