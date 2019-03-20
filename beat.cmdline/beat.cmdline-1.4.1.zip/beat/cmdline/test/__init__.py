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


# Basic setup for command test

import os
import sys
import tempfile
import shutil
import subprocess
import pkg_resources
import contextlib

import six.moves.urllib as urllib

from beat.core.test import tmp_prefix, teardown_package

platform = os.environ.get('BEAT_CMDLINE_TEST_PLATFORM', '')

disconnected = True
if platform:

  # the special name 'django' makes as believe it is connected
  if platform.startswith('django://'):
    # sets up django infrastructure, preloads test data
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', platform[9:])
    import django
    django.setup()

    # presets django database for tests
    from django.core.management import call_command
    call_command('install', 'test', interactive=False, verbose=1)

    disconnected = False

  else: #test it, actually
    # some patching to prevent common problems
    if not platform.endswith('/'): platform += '/'
    if not platform.startswith('http'): platform = 'http://' + platform
    try:
      code = urllib.request.urlopen(platform).getcode()
      disconnected = code != 200
    except (IOError, urllib.URLError):
      disconnected = True
else:
  platform = 'User did not set $BEAT_CMDLINE_TEST_PLATFORM'

user = 'user'
token = '4'


if sys.platform == 'darwin':
    prefix_folder = tempfile.mkdtemp(prefix=__name__,
                                     suffix='.prefix',
                                     dir='/tmp')
else:
    prefix_folder = tempfile.mkdtemp(prefix=__name__,
                                     suffix='.prefix')

prefix = os.path.join(prefix_folder, 'prefix')


def setup_package():
    prefixes = [
      pkg_resources.resource_filename('beat.backend.python.test', 'prefix'),
      pkg_resources.resource_filename('beat.core.test', 'prefix')
    ]

    for path in prefixes:
        subprocess.check_call(['rsync', '-arz', path, prefix_folder])


def teardown_package():
    shutil.rmtree(prefix_folder)


@contextlib.contextmanager
def temp_cwd():
    tempdir = tempfile.mkdtemp(prefix=__name__, suffix='.cwd')
    curdir = os.getcwd()
    os.chdir(tempdir)
    try: yield tempdir
    finally:
      os.chdir(curdir)
      shutil.rmtree(tempdir)
