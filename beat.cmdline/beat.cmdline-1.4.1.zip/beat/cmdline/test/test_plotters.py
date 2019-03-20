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


# Basic tests for the command line beat program: plotters

import os
import sys
import nose.tools
import shutil
import json
import simplejson
import collections
import click
from click.testing import CliRunner

from . import platform, disconnected, prefix, tmp_prefix, user, token
from .utils import index_experiment_dbs
from ..common import Selector
from beat.core.test.utils import slow, cleanup, skipif
from beat.cmdline.scripts import main_cli
from beat.core.plotter import Storage, Plotter


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
        '--user', user, '--cache', use_cache, '--platform', use_platform,
         'plotters'] + list(args)
    )
  if result.exit_code != 0:
      click.echo(result.output)
  return result.exit_code

@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one(obj=None):
  obj = obj or 'plot/bar/1'
  nose.tools.eq_(call('pull', obj, prefix=tmp_prefix), 0)
  s = Storage(tmp_prefix, obj)
  assert s.exists()
  return s


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_pull_one_check_deps(obj=None):
  obj = obj or 'plot/bar/1'
  nose.tools.eq_(call('pull', obj, prefix=tmp_prefix), 0)
  assert os.path.exists(os.path.join(tmp_prefix, 'plotterparameters', obj + '.json'))
  assert os.path.exists(os.path.join(tmp_prefix, 'libraries', 'plot/baselib/1' + '.json'))
  assert os.path.exists(os.path.join(tmp_prefix, 'dataformats', obj + '.json'))
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
def test_plot_sample_data_no_output_name():
  obj = 'plot/bar/1'
  test_pull_one()
  print(tmp_prefix)
  nose.tools.eq_(call('plot', obj, '--sample-data', prefix=tmp_prefix), 0)
  assert os.path.exists(os.path.join(tmp_prefix, 'plotters/' + obj.rsplit('/', 1)[0] + '/output_image.png'))


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_plot_sample_data_change_name():
  obj = 'plot/bar/1'
  test_pull_one()
  nose.tools.eq_(call('plot', obj, '--sample-data', '--output-image=test.png', prefix=tmp_prefix), 0)
  assert os.path.exists(os.path.join(tmp_prefix,'test.png'))


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_plot_sample_input_data_file():
  INPUT_DATA = '{"data":[{"label":"negative scores","x":[-5673.502545751196,-5417.040747386832,-5160.578949022467,-4904.117150658103,-4647.655352293739,-4391.193553929375,-4134.731755565012,-3878.269957200647,-3621.808158836283,-3365.346360471919,-3108.8845621075548,-2852.4227637431904,-2595.9609653788266,-2339.4991670144627,-2083.0373686500984,-1826.575570285734,-1570.1137719213702,-1313.6519735570064,-1057.1901751926425,-800.7283768282778],"y":[4.0,7.0,25.0,24.0,30.0,82.0,83.0,100.0,116.0,119.0,173.0,193.0,179.0,195.0,142.0,169.0,131.0,70.0,42.0,16.0]},{"label":"positivescores","x":[-1675.9012965728323,-1597.174480302131,-1518.44766403143,-1439.7208477607287,-1360.9940314900277,-1282.2672152193263,-1203.5403989486254,-1124.8135826779242,-1046.086766407223,-967.3599501365218,-888.6331338658206,-809.9063175951195,-731.1795013244183,-652.4526850537171,-573.725868783016,-494.99905251231485,-416.27223624161365,-337.54541997091246,-258.81860370021127,-180.09178742951008],"y":[1.0,3.0,2.0,0.0,0.0,1.0,1.0,3.0,3.0,2.0,2.0,7.0,13.0,7.0,11.0,13.0,11.0,11.0,6.0,3.0]}]}'

  with open(os.path.join(tmp_prefix, "temp_file.json"), "w") as f:
    f.write(INPUT_DATA)
  f.closed

  obj = 'plot/bar/1'
  test_pull_one()
  nose.tools.eq_(
      call('plot', obj,
           '--input-data=%s'%os.path.join(tmp_prefix, "temp_file.json"),
            '--output-image=test.png', prefix=tmp_prefix),
      0
  )
  assert os.path.exists(os.path.join(tmp_prefix,'test.png'))


@slow
@nose.tools.with_setup(teardown=cleanup)
@skipif(disconnected, "missing test platform (%s)" % platform)
def test_plot_plotterparameter(obj=None):
  obj = 'plot/bar/1'
  test_pull_one()
  assert os.path.exists(os.path.join(tmp_prefix, 'plotterparameters', obj + '.json'))

  with open(os.path.join(tmp_prefix, 'plotterparameters', obj + '.json'), 'r') as f:
      data = simplejson.load(f, object_pairs_hook=collections.OrderedDict)
  f.closed

  with open(os.path.join(tmp_prefix, 'plotterparameters', 'temp_file.json'), "w") as f:
    f.write(simplejson.dumps(data))
  f.closed

  nose.tools.eq_(
      call('plot', obj, '--sample-data', '--output-image=test.png',
           '--plotter-parameter=temp_file', prefix=tmp_prefix),
      0
  )
  assert os.path.exists(os.path.join(tmp_prefix,'test.png'))
