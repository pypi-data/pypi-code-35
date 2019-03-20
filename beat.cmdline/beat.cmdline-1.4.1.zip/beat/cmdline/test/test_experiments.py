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


# Basic tests for the command line beat program: experiments

import os
import sys
import logging
import nose.tools
import click
from click.testing import CliRunner
from . import platform, disconnected, prefix, tmp_prefix, user, token, temp_cwd
from .utils import index_experiment_dbs, MockLoggingHandler
from ..common import Selector
from beat.cmdline.scripts import main_cli
from beat.core.test.utils import slow, cleanup, skipif
from beat.core.experiment import Storage, Experiment


def setup_experiments():
  index_experiment_dbs('user/user/double_triangle/1/double_triangle')
  index_experiment_dbs('user/user/integers_addition/1/integers_addition')


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''

  use_prefix = kwargs.get('prefix', prefix)
  use_platform = kwargs.get('platform', platform)
  use_cache = kwargs.get('cache', 'cache')

  runner = CliRunner()
  with runner.isolated_filesystem():
    result = runner.invoke(
        main_cli.main,
        ['--test-mode', '--prefix', use_prefix, '--token', token,
        '--user', user, '--platform', use_platform, '--cache', use_cache,
        'experiments'] +
        list(args)
    )
  if result.exit_code != 0:
      click.echo(result.output)
  return result.exit_code


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_remote_list():
  nose.tools.eq_(call('list', '--remote'), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one(obj=None):
  obj = obj or 'user/user/single/1/single'
  nose.tools.eq_(call('pull', obj, prefix=tmp_prefix), 0)
  s = Storage(tmp_prefix, obj)
  assert s.exists()
  return s


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_all():
  nose.tools.eq_(call('pull', prefix=tmp_prefix), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_diff():
  obj = 'user/user/single/1/single'
  nose.tools.eq_(call('pull', obj, prefix=tmp_prefix), 0)

  s = Storage(tmp_prefix, obj)
  assert s.exists()

  # quickly modify the user experiment:
  f = Experiment(tmp_prefix, obj)
  f.data['globals']['queue'] = 'another_queue'
  f.write()

  nose.tools.eq_(call('diff', obj, prefix=tmp_prefix), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_status():
  test_diff()
  test_pull_one()
  nose.tools.eq_(call('status', prefix=tmp_prefix), 0)


def test_check_valid():
  obj = 'user/user/single/1/single'
  nose.tools.eq_(call('check', obj), 0)


def test_check_invalid():
  obj = 'user/user/single/1/does_not_exist'
  nose.tools.eq_(call('check', obj), 1)


@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_fork(obj=None, obj2=None):
  obj = obj or 'user/user/single/1/single'
  test_pull_one(obj)
  obj2 = obj2 or 'user/user/single/1/different'
  nose.tools.eq_(call('fork', obj, obj2, prefix=tmp_prefix), 0)
  s = Storage(tmp_prefix, obj2)
  assert s.exists()

  # check fork status
  with Selector(tmp_prefix) as selector:
    assert selector.forked_from('experiment', obj2) == obj


@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_delete_local():
  obj = 'user/user/single/1/single'
  storage = test_pull_one(obj)
  nose.tools.eq_(call('rm', obj, prefix=tmp_prefix), 0)
  assert not storage.exists()


@slow
@nose.tools.with_setup(setup=setup_experiments, teardown=cleanup)
def test_run_integers_addition_1():
  obj = 'user/user/integers_addition/1/integers_addition'
  nose.tools.eq_(call('run', obj, cache=tmp_prefix), 0)


@slow
@nose.tools.with_setup(setup=setup_experiments, teardown=cleanup)
def test_list_integers_addition_1_cache():
  obj = 'user/user/integers_addition/1/integers_addition'
  nose.tools.eq_(call('run', obj, cache=tmp_prefix), 0)
  nose.tools.eq_(call('caches', '--list', obj, cache=tmp_prefix), 0)


@slow
@nose.tools.with_setup(setup=setup_experiments, teardown=cleanup)
def test_checksum_integers_addition_1_cache():
  obj = 'user/user/integers_addition/1/integers_addition'
  nose.tools.eq_(call('run', obj, cache=tmp_prefix), 0)
  nose.tools.eq_(call('caches', '--checksum', obj, cache=tmp_prefix), 0)


@slow
@nose.tools.with_setup(setup=setup_experiments, teardown=cleanup)
def test_delete_integers_addition_1_cache():
  obj = 'user/user/integers_addition/1/integers_addition'
  nose.tools.eq_(call('run', obj, cache=tmp_prefix), 0)
  nose.tools.eq_(call('caches', '--delete', obj, cache=tmp_prefix), 0)


@slow
@nose.tools.with_setup(setup=setup_experiments, teardown=cleanup)
def test_run_integers_addition_1_twice():
  log_handler = MockLoggingHandler(level='DEBUG')
  logging.getLogger().addHandler(log_handler)
  log_messages = log_handler.messages

  obj = 'user/user/integers_addition/1/integers_addition'
  nose.tools.eq_(call('run', obj, cache=tmp_prefix), 0)
  info_len = len(log_messages['info'])
  nose.tools.eq_(info_len, 5)
  assert log_messages['info'][info_len - 1].startswith('  Results')
  nose.tools.eq_(call('run', obj, cache=tmp_prefix), 0)
  info_len = len(log_messages['info'])
  nose.tools.eq_(info_len, 8)
  assert log_messages['info'][info_len - 1].startswith('  Results')


@slow
@nose.tools.with_setup(setup=setup_experiments, teardown=cleanup)
def test_run_double_triangle_1():
  obj = 'user/user/double_triangle/1/double_triangle'
  nose.tools.eq_(call('run', obj, cache=tmp_prefix), 0)


@slow
@nose.tools.with_setup(setup=setup_experiments, teardown=cleanup)
def test_run_single_error_1_local():
  # When running locally, the module with the error is loaded
  # inside the currently running process and will return '1'.
  obj = 'user/user/single/1/single_error'
  nose.tools.eq_(call('run', obj, '--local', cache=tmp_prefix), 1)


@slow
@nose.tools.with_setup(setup=setup_experiments, teardown=cleanup)
def test_run_single_error_twice_local():
  # This one makes sure our output reset is working properly. Both tries should
  # give out the same error.
  obj = 'user/user/single/1/single_error'
  nose.tools.eq_(call('run', obj, '--local', cache=tmp_prefix), 1)
  nose.tools.eq_(call('run', obj, '--local', cache=tmp_prefix), 1)


@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_push_and_delete():
  obj = 'user/user/single/1/single'
  obj2 = 'user/user/single/1/different'
  test_fork(obj, obj2)

  # now push the fork and then delete it remotely
  nose.tools.eq_(call('push', obj2, prefix=tmp_prefix), 0)
  nose.tools.eq_(call('rm', '--remote', obj2, prefix=tmp_prefix), 0)


@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_draw():
  obj = 'user/user/double_triangle/1/double_triangle'
  test_pull_one(obj)

  # now push the new object and then delete it remotely
  nose.tools.eq_(call('draw', '--path=%s' % tmp_prefix, prefix=tmp_prefix), 0)

  assert os.path.exists(os.path.join(tmp_prefix, 'experiments', obj + '.dot'))
  assert os.path.exists(os.path.join(tmp_prefix, 'experiments', obj + '.png'))
