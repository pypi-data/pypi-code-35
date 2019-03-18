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


import nose.tools
from ..database import Database

from . import prefix


#----------------------------------------------------------


def load(database_name):

    database = Database(prefix, database_name)
    assert database.valid
    return database


#----------------------------------------------------------


def test_load_valid_database():

    database = Database(prefix, 'integers_db/1')
    assert database.valid, '\n  * %s' % '\n  * '.join(database.errors)

    nose.tools.eq_(len(database.sets("double")), 1)
    nose.tools.eq_(len(database.sets("triple")), 1)
    nose.tools.eq_(len(database.sets("two_sets")), 2)


#----------------------------------------------------------


def test_load_protocol_with_one_set():

    database = Database(prefix, 'integers_db/1')

    protocol = database.protocol("double")
    nose.tools.eq_(len(protocol['sets']), 1)

    set = database.set("double", "double")

    nose.tools.eq_(set['name'], 'double')
    nose.tools.eq_(len(set['outputs']), 3)

    assert set['outputs']['a'] is not None
    assert set['outputs']['b'] is not None
    assert set['outputs']['sum'] is not None


#----------------------------------------------------------


def test_load_protocol_with_two_sets():

    database = Database(prefix, 'integers_db/1')

    protocol = database.protocol("two_sets")
    nose.tools.eq_(len(protocol['sets']), 2)

    set = database.set("two_sets", "double")

    nose.tools.eq_(set['name'], 'double')
    nose.tools.eq_(len(set['outputs']), 3)

    assert set['outputs']['a'] is not None
    assert set['outputs']['b'] is not None
    assert set['outputs']['sum'] is not None

    set = database.set("two_sets", "triple")

    nose.tools.eq_(set['name'], 'triple')
    nose.tools.eq_(len(set['outputs']), 4)

    assert set['outputs']['a'] is not None
    assert set['outputs']['b'] is not None
    assert set['outputs']['c'] is not None
    assert set['outputs']['sum'] is not None
