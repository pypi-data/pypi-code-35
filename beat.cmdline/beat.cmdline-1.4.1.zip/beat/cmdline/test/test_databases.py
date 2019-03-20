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


# Basic tests for the command line beat program: databases

import nose.tools
import click
from click.testing import CliRunner
from . import platform, disconnected, prefix, tmp_prefix, user, token, temp_cwd

from beat.cmdline.scripts import main_cli
from beat.core.test.utils import slow, cleanup, skipif
from beat.core.database import Storage, Database


def index_integer_db():
    call('index', 'integers_db/1')


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''

  use_prefix = kwargs.get('prefix', prefix)
  use_platform = kwargs.get('platform', platform)

  runner = CliRunner()
  with runner.isolated_filesystem():
    result = runner.invoke(
        main_cli.main,
        ['--test-mode', '--prefix', use_prefix, '--token', token,
        '--user', user, '--platform', use_platform, 'databases'] +
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


@nose.tools.with_setup(teardown=cleanup)
def test_local_list():
  nose.tools.eq_(call('list'), 0)


@nose.tools.nottest
@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one():
  obj = 'simple/1'
  nose.tools.eq_(call('pull', obj, prefix=tmp_prefix), 0)
  s = Storage(tmp_prefix, obj)
  assert s.exists()


@nose.tools.nottest
@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_all():
  nose.tools.eq_(call('pull', prefix=tmp_prefix), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_diff():
  obj = 'simple/1'
  nose.tools.eq_(call('pull', obj, prefix=tmp_prefix), 0)

  # quickly modify the user algorithm by emptying it
  f = Database(tmp_prefix, obj)
  nose.tools.eq_(len(f.errors), 0, 'Failed to load Database: \n%s' % '\n'.join(f.errors))
  f.data['root_folder'] = '/a/different/path'
  f.write()

  nose.tools.eq_(call('diff', obj, prefix=tmp_prefix), 0)


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_status():
  test_diff()
  nose.tools.eq_(call('status', prefix=tmp_prefix), 0)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_good():
  nose.tools.eq_(call('view', 'integers_db/1/double/double'), 0)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_unknown_protocol():

  nose.tools.eq_(call('view', 'integers_db/1/single/double'), 1)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_unknown_set():
  nose.tools.eq_(call('view', 'integers_db/1/double/single'), 1)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_bad():
  nose.tools.eq_(call('view', 'integers_db/1/two_sets'), 1)


@nose.tools.with_setup(setup=index_integer_db, teardown=cleanup)
def test_view_invalid():
  nose.tools.eq_(call('view', 'invalid/1/default/set'), 1)


def test_index_unknown_database():
  nose.tools.eq_(call('index', 'foobar/1'), 1)


@nose.tools.with_setup(teardown=cleanup)
def test_index_good():
  nose.tools.eq_(call('index', 'integers_db/1'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_list_index_good():
  nose.tools.eq_(call('index', 'integers_db/1'), 0)
  nose.tools.eq_(call('index', '--list', 'integers_db/1'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_delete_index_good():
  nose.tools.eq_(call('index', 'integers_db/1'), 0)
  nose.tools.eq_(call('index', '--delete', 'integers_db/1'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_index_all(): #bad and good, return != 0
  expected_errors = 16
  existing_errors = call('index')
  assert existing_errors >= expected_errors, "There should be at least %d " \
      "errors on installed databases, but I've found only %d" % \
      (expected_errors, existing_errors)
