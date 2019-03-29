#    This file is part of KTBS <http://liris.cnrs.fr/sbt-dev/ktbs>
#    Copyright (C) 2015 Francoise Conil <fconil@liris.cnrs.fr> /
#    Universite de Lyon, CNRS <http://www.universite-lyon.fr>
#
#    KTBS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    KTBS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with KTBS.  If not, see <http://www.gnu.org/licenses/>.

"""
I provide kTBS CSV serializer, this is a serialization with information loss.
"""
from cgi import escape as cgi_escape
from rdfrest.serializers import register_serializer, SerializeError
from rdfrest.util import wrap_exceptions
from re import compile as Regexp

from ..namespace import KTBS, KTBS_NS_URI
from ..serpar.csv_serializers import iter_csv_rows, LAST_PART

CTYPE = "text/html"

@wrap_exceptions(SerializeError)
def serialize_ktbs4la(graph, resource, bindings=None, highlight=None):

    yield '''
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <script src="https://liris-ktbs01.insa-lyon.fr:8000/ktbs4la/bower_components/webcomponentsjs/webcomponents-lite.js"></script>

  <!-- INIT POLYMER -->
  <script>
    window.Polymer = window.Polymer || {};
    window.Polymer.dom = 'shadow';
  </script>

  <!-- import a component that relies on Polymer -->
  <link rel="import" href="https://liris-ktbs01.insa-lyon.fr:8000/ktbs4la/bower_components/polymer/polymer.html">
  <link rel="import" href="https://liris-ktbs01.insa-lyon.fr:8000/ktbs4la/bower_components/ktbs-for-la/ktbs-for-la.html">

  <!-- Moar css -->
  <style>
    body{
      margin: 0;
      padding: 0;
    }
  </style>
</head>

<body>
  <ktbs-for-la ktbs-url="%s"></ktbs-for-la>
</body>
</html>
    ''' % resource.uri.encode('utf8')

def start_plugin(config):
    register_serializer(CTYPE, None, 99, KTBS.KtbsRoot)(serialize_ktbs4la)
