# -*- coding: utf-8 -*-
__author__ = 'luckydonald'


from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import Http404
from ...logger import logging  # pip install luckydonald-utils
from ...dependencies import import_or_install
logger = logging.getLogger(__name__)

import_or_install("IPy", "IPy")
from IPy import IP  # pip install IPy


class AllowFromMiddleware(object):
	"""
	Allow only given IPs to access, else raise a `Http404` error. Is ignoren when `DEBUG` is `True`.
	It will be checked if a ip start with anything in the settings.ALLOW_FROM string.

	Example:
	The *`settings.py`*
	```
	ALLOW_FROM = ["8.8.8.8", "134.169.0.0/16"]
	```
	```"134.169.0.0/16"
	Some examples what IP that will allow:
		- `8.8.8.8`,
		- `123.2.0.1` (which is `123.002.000.001`, keep that in mind!)
		- `123.20.0.1`
		- `123.200.0.1`
		- `123.255.0.1`
		- `123.255.123.75`


	Notice, this **only** checks the *beginning of string*, no IP range whatsoever.
	Also, asterisks ("*") are cut, and only the string before is used.

	Mimics the Apache syntax:
	> Allow from 134.169.
	One would write as
	>>> ALLOW_FROM = ["134.169."]
	in the `settings.py`.

	"""
	buffered_ALLOW_FROM = None

	def process_request(self, request):
		if self.buffered_ALLOW_FROM is None:
			self.buffered_ALLOW_FROM = []
			for ip in settings.ALLOW_FROM:
				self.buffered_ALLOW_FROM.append(IP(ip))
			#end for
		#end if
		remote_addr = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', None))
		if any([remote_addr in ip for ip in self.buffered_ALLOW_FROM]):
			if settings.DEBUG:
				logger.debug("The IP {remote_addr} should not be allowed, but is served anyway because DEBUG=True.".format(remote_addr=remote_addr))
			else:
				raise Http404
			#end if DEBUG
		#end if
	#end def
#end class