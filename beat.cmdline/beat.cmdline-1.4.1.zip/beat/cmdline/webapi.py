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


import socket
import traceback

import six
import simplejson

import logging


logger = logging.getLogger(__name__)


class WebAPI(object):
  """Manages all the interactions with the Web API
  """

  def __init__(self, platform, user, token):
    self.platform = platform
    self.parsed = six.moves.urllib.parse.urlparse(self.platform)
    self.user = user
    self.token = token
    if self.token is None: self.user = '**anonymous**'
    self.connection = None
    self.users = 0 #usage counter for the current connection

  def connect(self):
    """Establish a connection with the Web API
    """

    if self.connection is not None:
      self.users += 1
      return

    if not self.platform:
      logger.error("No `platform' set up. Set it with " \
                   "`beat config platform <url>'")
      return

    port = self.parsed.port
    if port is None:
      if self.parsed.scheme.lower() == 'https': port = 443
      else: port = 80

    connector = six.moves.http_client.HTTPConnection
    if self.parsed.scheme.lower() == 'https':
        connector = six.moves.http_client.HTTPSConnection
    self.connection = connector(self.parsed.hostname, port)

    try:
      self.connection.connect()
    except socket.error as ex:
      logger.error('Failed to establish a connection with the Web API, ' \
                   'reason: %s', ex.strerror)
      self.connection = None
    except:
      logger.error('Failed to establish a connection with the Web API, ' \
                   'reason: %s', traceback.format_exc())
      self.connection = None

    self.users += 1 #this should be the first user


  def is_anonymous(self):
    """Tells if the user has not set credentials for accessing the platform"""
    return self.token is None


  def disconnect(self):
    """Disconnects from the remote server"""

    self.users -= 1

    if self.users <= 0 and self.connected:
      self.connection.close()
      self.connection = None


  @property
  def connected(self):
    """``True`` if it is connected to the Web-API. ``False`` otherwise"""
    return self.connection is not None


  def __enter__(self):
    self.connect()
    return self

  def __exit__(self, *exc):
    self.disconnect()


  def _make_path(self, path):

    url = self.parsed.path
    if url != '':
      if url[0] != '/': url = '/' + url
      if url[-1] == '/': url = url[:-1]
    if path[0] == '/': path = path[1:]
    return url + '/' + path


  def _make_headers(self):
    """Return the headers
    """

    if self.token is None: return {}

    return {
        'Authorization': 'Token %s' % (self.token),
    }


  def _message(self, type, url, data=None):
    """Sends a message to the Web-API"""

    # Establish the connection
    if not self.connected: return (None, None)

    # Setup the request
    headers = self._make_headers()

    if data is not None:
      data = simplejson.dumps(data)
      headers['Content-Type'] = 'application/json'
      headers['Content-Length'] = len(data)

    # Send the request
    try:
      url = self._make_path(url)
      logger.debug("[%s] `%s://%s%s' with secret token...",
                   type.upper(), self.parsed.scheme, self.parsed.hostname, url)
      self.connection.request(type, url, data, headers)
      response = self.connection.getresponse()
      logger.debug("response status code is `%d': %s", response.status,
                   response.reason)
    except:
      logger.error("Failed to use the web API, reason: %s",
                   traceback.format_exc())
      self.disconnect()
      return (None, None)

    return (response.status, response.read())


  def get(self, url):
    return self._message('GET', url)

  def post(self, url, data=None):
    return self._message('POST', url, data)

  def put(self, url, data):
    return self._message('PUT', url, data)

  def delete(self, url):
    return self._message('DELETE', url)
