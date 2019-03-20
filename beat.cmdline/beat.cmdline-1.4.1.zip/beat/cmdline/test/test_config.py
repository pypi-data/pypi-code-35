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


# Basic tests for the command line beat program: config

import os
import click
from click.testing import CliRunner
import nose.tools
from nose.tools import assert_raises
import simplejson

from . import tmp_prefix, temp_cwd
from beat.core.test.utils import cleanup
from .. import config
from .. import common
from beat.cmdline.scripts import main_cli


def call(*args, **kwargs):
  '''A central mechanism to call the main routine with the right parameters'''
  use_prefix = kwargs.get('prefix', tmp_prefix)

  runner = CliRunner()
  result = runner.invoke(
    main_cli.main,
    ['--test-mode', '--prefix', use_prefix] +
    list(args)
  )
  if result.exit_code != 0:
      click.echo(result.output)
  return result.exit_code


def test_config_list():
  nose.tools.eq_(call('config', 'show'), 0)


def test_config_cache():
  cache_dir = 'cache'

  c = config.Configuration({'--cache': cache_dir})
  nose.tools.eq_(c.cache, os.path.join(c.path, cache_dir))

  cache_dir = '/an/absolute/cache/dir'
  c = config.Configuration({'--cache': cache_dir})
  nose.tools.eq_(c.cache, cache_dir)


@nose.tools.with_setup(teardown=cleanup)
def test_set_local_token():
  token_value = '123456abcdefffff'
  nose.tools.eq_(call('config', 'set', '--local', 'token', token_value), 0)
  config = '.beatrc'
  assert os.path.exists(config)
  with open(config, 'rt') as f: contents = simplejson.load(f)
  assert contents['token'] == token_value


@nose.tools.with_setup(teardown=cleanup)
def test_set_local_multiple():
  token_value = '123456abcde123456abcde123456abcdefff123456abcdef'
  nose.tools.eq_(call('config', 'set', '--local', 'token', token_value), 0)
  config = '.beatrc'
  assert os.path.exists(config)
  with open(config, 'rt') as f: contents = simplejson.load(f)
  assert contents['token'] == token_value

  # then we reduce the token size and see if the written file gets messed-up
  token_value = '123456'
  nose.tools.eq_(call('config', 'set', '--local', 'token', token_value), 0)
  assert os.path.exists(config)
  with open(config, 'rt') as f: contents = simplejson.load(f)
  assert contents['token'] == token_value


@nose.tools.with_setup(teardown=cleanup)
def test_set_local_atnt_db():
  db_config = 'database/atnt'
  db_path = './atnt_db'
  nose.tools.eq_(call('config', 'set', '--local', db_config, db_path), 0)
  config = '.beatrc'
  assert os.path.exists(config)
  with open(config, 'rt') as f: contents = simplejson.load(f)
  assert contents[db_config] == db_path


@nose.tools.with_setup(teardown=cleanup)
def test_set_get_local_atnt_db():
  db_config = 'database/atnt'
  db_path = './atnt_db'
  nose.tools.eq_(call('config', 'set', '--local', db_config, db_path), 0)
  nose.tools.eq_(call('config', 'get', db_config), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_set_bad_config_key():
  db_config = 'fail'
  nose.tools.assert_not_equal(call('config', 'set', '--local', db_config, db_config), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_get_bad_config_key():
  db_config = 'fail'
  nose.tools.assert_not_equal(call('config', 'get', db_config), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_get_token():
  nose.tools.eq_(call('config', 'set', '--local', 'token', '12we3f45fgh'), 0)
  nose.tools.eq_(call('config', 'get', 'token'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_get_editor():
  nose.tools.eq_(call('config', 'set', '--local', 'editor', 'vi'), 0)
  nose.tools.eq_(call('config', 'get', 'editor'), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_set_local_editor():
  editor_value = 'editor'
  with temp_cwd() as d:
    nose.tools.eq_(call('config', 'set', '--local', 'editor', editor_value), 0)
    config = os.path.join(d, '.beatrc')
    assert os.path.exists(config)
    with open(config, 'rt') as f: contents = simplejson.load(f)
    assert contents['editor'] == editor_value


def create_touch_file(tmp_prefix, editor):
  cmd = "%s %s && %s %s" % ('mkdir -p', os.path.join(tmp_prefix, 'plotters'), 'touch', os.path.join(tmp_prefix, 'plotters', 'test.py'))
  os.system(cmd)
  result = common.edit_local_file(tmp_prefix, editor, 'plotter', "test")
  return result


def read_data(tmp_prefix):
  with open(os.path.join(tmp_prefix, 'plotters', 'test.py'), 'r') as f:
      read_data = f.read().split('\n')[0]
  f.closed
  return read_data


def clean_tmp_files(tmp_prefix):
  cmd = "%s %s" % ('rm -fr', os.path.join(tmp_prefix, 'plotters'))
  os.system(cmd)


@nose.tools.with_setup(teardown=cleanup)
def test_check_editor_system_no_editor_set():
  editor = None
  os.environ['VISUAL'] = ''
  os.environ['EDITOR'] = ''

  result = create_touch_file(tmp_prefix, editor)
  assert result == 1

  data = read_data(tmp_prefix)
  assert len(data) == 0

  clean_tmp_files(tmp_prefix)


@nose.tools.with_setup(teardown=cleanup)
def test_check_editor_system_no_local_editor():
  editor = None
  os.environ['VISUAL'] = 'echo "2" >'
  os.environ['EDITOR'] = 'echo "3" >'

  result = create_touch_file(tmp_prefix, editor)
  assert result == 0

  data = read_data(tmp_prefix)
  assert len(data) == 1
  assert data == "2"

  clean_tmp_files(tmp_prefix)


@nose.tools.with_setup(teardown=cleanup)
def test_check_editor_system_local_editor_set():
  editor = 'echo "1" >'
  os.environ['VISUAL'] = 'echo "2" >'
  os.environ['EDITOR'] = 'echo "3" >'

  result = create_touch_file(tmp_prefix, editor)
  assert result == 0

  data = read_data(tmp_prefix)
  assert len(data) == 1
  assert data == "1"

  clean_tmp_files(tmp_prefix)


@nose.tools.with_setup(teardown=cleanup)
def test_check_editor_system_no_local_editor_no_visual():
  editor = None
  os.environ['VISUAL'] = ''
  os.environ['EDITOR'] = 'echo "3" >'

  result = create_touch_file(tmp_prefix, editor)
  assert result == 0

  data = read_data(tmp_prefix)
  assert len(data) == 1
  assert data == "3"

  clean_tmp_files(tmp_prefix)
