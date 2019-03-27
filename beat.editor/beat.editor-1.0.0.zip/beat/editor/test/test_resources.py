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

# test the resources.py file
# (mostly endpoints and working with the filesystem)

import nose.tools
import os

from .. import resources

# the func names the endpoint the given name
def test_check_valid_generated_endpoint_name():
    name = 'TestEndpoint'
    endpoint = resources.gen_endpoint(name)
    nose.tools.eq_(endpoint.__name__, name)

# the func doesnt accept non-entity names
@nose.tools.raises(AssertionError)
def test_assert_valid_entity_invalid():
    resources.assert_valid_entity('notanentity')

# the func parses this file
def test_path_to_dict_file():
    currfile = os.path.realpath(__file__)
    res = resources.path_to_dict(currfile)
    # in python 3 the first case works but in python 2 the second case works
    assert res == {'name': 'test_resources.py', 'type': 'file'} or res == {'name': 'test_resources.pyc', 'type': 'file'}

# the func parses this folder
def test_path_to_dict_folder():
    currfolder = os.path.dirname(os.path.realpath(__file__))
    res = resources.path_to_dict(currfolder)
    nose.tools.eq_(res['name'], 'test')
    nose.tools.eq_(res['type'], 'directory')
    nose.tools.ok_({'name': '__init__.py', 'type': 'file'} in res['children'])
    nose.tools.ok_({'name': 'test_resources.py', 'type': 'file'} in res['children'])

