# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
kallithea.lib.auth_modules.auth_ldap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kallithea authentication plugin for LDAP

This file was forked by the Kallithea project in July 2014.
Original author and date, and relevant copyright and licensing information is below:
:created_on: Created on Nov 17, 2010
:author: marcink
:copyright: (c) 2013 RhodeCode GmbH, and others.
:license: GPLv3, see LICENSE.md for more details.
"""


import logging
import traceback

from kallithea.lib import auth_modules
from kallithea.lib.compat import hybrid_property
from kallithea.lib.utils2 import safe_unicode, safe_str
from kallithea.lib.exceptions import (
    LdapConnectionError, LdapUsernameError, LdapPasswordError, LdapImportError
)
from kallithea.model.db import User

log = logging.getLogger(__name__)

try:
    import ldap
    import ldap.filter
except ImportError:
    # means that python-ldap is not installed
    ldap = None


class AuthLdap(object):

    def __init__(self, server, base_dn, port=None, bind_dn='', bind_pass='',
                 tls_kind='LDAPS', tls_reqcert='DEMAND', cacertdir=None, ldap_version=3,
                 ldap_filter='(&(objectClass=user)(!(objectClass=computer)))',
                 search_scope='SUBTREE', attr_login='uid'):
        if ldap is None:
            raise LdapImportError

        self.ldap_version = ldap_version

        self.TLS_KIND = tls_kind
        OPT_X_TLS_DEMAND = 2
        self.TLS_REQCERT = getattr(ldap, 'OPT_X_TLS_%s' % tls_reqcert,
                                   OPT_X_TLS_DEMAND)
        self.cacertdir = cacertdir

        protocol = 'ldaps' if self.TLS_KIND == 'LDAPS' else 'ldap'
        if not port:
            port = 636 if self.TLS_KIND == 'LDAPS' else 389
        self.LDAP_SERVER = str(', '.join(
            "%s://%s:%s" % (protocol,
                            host.strip(),
                            port)
            for host in server.split(',')))

        self.LDAP_BIND_DN = safe_str(bind_dn)
        self.LDAP_BIND_PASS = safe_str(bind_pass)

        self.BASE_DN = safe_str(base_dn)
        self.LDAP_FILTER = safe_str(ldap_filter)
        self.SEARCH_SCOPE = getattr(ldap, 'SCOPE_%s' % search_scope)
        self.attr_login = attr_login

    def authenticate_ldap(self, username, password):
        """
        Authenticate a user via LDAP and return his/her LDAP properties.

        Raises AuthenticationError if the credentials are rejected, or
        EnvironmentError if the LDAP server can't be reached.

        :param username: username
        :param password: password
        """

        if not password:
            log.debug("Attempt to authenticate LDAP user "
                      "with blank password rejected.")
            raise LdapPasswordError()
        if "," in username:
            raise LdapUsernameError("invalid character in username: ,")
        try:
            if self.cacertdir:
                if hasattr(ldap, 'OPT_X_TLS_CACERTDIR'):
                    ldap.set_option(ldap.OPT_X_TLS_CACERTDIR, self.cacertdir)
                else:
                    log.debug("OPT_X_TLS_CACERTDIR is not available - can't set %s", self.cacertdir)
            ldap.set_option(ldap.OPT_REFERRALS, ldap.OPT_OFF)
            ldap.set_option(ldap.OPT_RESTART, ldap.OPT_ON)
            ldap.set_option(ldap.OPT_TIMEOUT, 20)
            ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, 10)
            ldap.set_option(ldap.OPT_TIMELIMIT, 15)
            if self.TLS_KIND != 'PLAIN':
                ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, self.TLS_REQCERT)
            server = ldap.initialize(self.LDAP_SERVER)
            if self.ldap_version == 2:
                server.protocol = ldap.VERSION2
            else:
                server.protocol = ldap.VERSION3

            if self.TLS_KIND == 'START_TLS':
                server.start_tls_s()

            if self.LDAP_BIND_DN and self.LDAP_BIND_PASS:
                log.debug('Trying simple_bind with password and given DN: %s',
                          self.LDAP_BIND_DN)
                server.simple_bind_s(self.LDAP_BIND_DN, self.LDAP_BIND_PASS)

            filter_ = '(&%s(%s=%s))' % (self.LDAP_FILTER,
                                        ldap.filter.escape_filter_chars(self.attr_login),
                                        ldap.filter.escape_filter_chars(username))
            log.debug("Authenticating %r filter %s at %s", self.BASE_DN,
                      filter_, self.LDAP_SERVER)
            lobjects = server.search_ext_s(self.BASE_DN, self.SEARCH_SCOPE,
                                           filter_)

            if not lobjects:
                raise ldap.NO_SUCH_OBJECT()

            for (dn, _attrs) in lobjects:
                if dn is None:
                    continue

                try:
                    log.debug('Trying simple bind with %s', dn)
                    server.simple_bind_s(dn, safe_str(password))
                    results = server.search_ext_s(dn, ldap.SCOPE_BASE,
                                                  '(objectClass=*)')
                    if len(results) == 1:
                        dn_, attrs = results[0]
                        assert dn_ == dn
                        return dn, attrs

                except ldap.INVALID_CREDENTIALS:
                    log.debug("LDAP rejected password for user '%s': %s",
                              username, dn)
                    continue # accept authentication as another ldap user with same username

            log.debug("No matching LDAP objects for authentication "
                      "of '%s'", username)
            raise LdapPasswordError()

        except ldap.NO_SUCH_OBJECT:
            log.debug("LDAP says no such user '%s'", username)
            raise LdapUsernameError()
        except ldap.SERVER_DOWN:
            # [0] might be {'info': "TLS error -8179:Peer's Certificate issuer is not recognized.", 'desc': "Can't contact LDAP server"}
            raise LdapConnectionError("LDAP can't connect to authentication server")


class KallitheaAuthPlugin(auth_modules.KallitheaExternalAuthPlugin):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._tls_kind_values = ["PLAIN", "LDAPS", "START_TLS"]
        self._tls_reqcert_values = ["NEVER", "ALLOW", "TRY", "DEMAND", "HARD"]
        self._search_scopes = ["BASE", "ONELEVEL", "SUBTREE"]

    @hybrid_property
    def name(self):
        return "ldap"

    def settings(self):
        settings = [
            {
                "name": "host",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "string",
                "description": "Host of the LDAP Server",
                "formname": "LDAP Host"
            },
            {
                "name": "port",
                "validator": self.validators.Number(strip=True),
                "type": "string",
                "description": "Port that the LDAP server is listening on. Defaults to 389 for PLAIN/START_TLS and 636 for LDAPS.",
                "default": "",
                "formname": "Custom LDAP Port"
            },
            {
                "name": "dn_user",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "string",
                "description": "User to connect to LDAP",
                "formname": "Account"
            },
            {
                "name": "dn_pass",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "password",
                "description": "Password to connect to LDAP",
                "formname": "Password"
            },
            {
                "name": "tls_kind",
                "validator": self.validators.OneOf(self._tls_kind_values),
                "type": "select",
                "values": self._tls_kind_values,
                "description": "TLS Type",
                "default": 'LDAPS',
                "formname": "Connection Security"
            },
            {
                "name": "tls_reqcert",
                "validator": self.validators.OneOf(self._tls_reqcert_values),
                "type": "select",
                "values": self._tls_reqcert_values,
                "description": "Require Cert over TLS?",
                "formname": "Certificate Checks"
            },
            {
                "name": "cacertdir",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "string",
                "description": "Optional: Custom CA certificate directory for validating LDAPS",
                "formname": "Custom CA Certificates"
            },
            {
                "name": "base_dn",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "string",
                "description": "Base DN to search (e.g., dc=mydomain,dc=com)",
                "formname": "Base DN"
            },
            {
                "name": "filter",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "string",
                "description": "Filter to narrow results (e.g., ou=Users, etc)",
                "formname": "LDAP Search Filter"
            },
            {
                "name": "search_scope",
                "validator": self.validators.OneOf(self._search_scopes),
                "type": "select",
                "values": self._search_scopes,
                "description": "How deep to search LDAP",
                "formname": "LDAP Search Scope"
            },
            {
                "name": "attr_login",
                "validator": self.validators.AttrLoginValidator(not_empty=True, strip=True),
                "type": "string",
                "description": "LDAP Attribute to map to user name",
                "formname": "Login Attribute"
            },
            {
                "name": "attr_firstname",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "string",
                "description": "LDAP Attribute to map to first name",
                "formname": "First Name Attribute"
            },
            {
                "name": "attr_lastname",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "string",
                "description": "LDAP Attribute to map to last name",
                "formname": "Last Name Attribute"
            },
            {
                "name": "attr_email",
                "validator": self.validators.UnicodeString(strip=True),
                "type": "string",
                "description": "LDAP Attribute to map to email address",
                "formname": "Email Attribute"
            }
        ]
        return settings

    def use_fake_password(self):
        return True

    def auth(self, userobj, username, password, settings, **kwargs):
        """
        Given a user object (which may be null), username, a plaintext password,
        and a settings object (containing all the keys needed as listed in settings()),
        authenticate this user's login attempt.

        Return None on failure. On success, return a dictionary of the form:

            see: KallitheaAuthPluginBase.auth_func_attrs
        This is later validated for correctness
        """

        if not username or not password:
            log.debug('Empty username or password skipping...')
            return None

        kwargs = {
            'server': settings.get('host', ''),
            'base_dn': settings.get('base_dn', ''),
            'port': settings.get('port'),
            'bind_dn': settings.get('dn_user'),
            'bind_pass': settings.get('dn_pass'),
            'tls_kind': settings.get('tls_kind'),
            'tls_reqcert': settings.get('tls_reqcert'),
            'cacertdir': settings.get('cacertdir'),
            'ldap_filter': settings.get('filter'),
            'search_scope': settings.get('search_scope'),
            'attr_login': settings.get('attr_login'),
            'ldap_version': 3,
        }

        if kwargs['bind_dn'] and not kwargs['bind_pass']:
            log.debug('Using dynamic binding.')
            kwargs['bind_dn'] = kwargs['bind_dn'].replace('$login', username)
            kwargs['bind_pass'] = password
        log.debug('Checking for ldap authentication')

        try:
            aldap = AuthLdap(**kwargs)
            (user_dn, ldap_attrs) = aldap.authenticate_ldap(username, password)
            log.debug('Got ldap DN response %s', user_dn)

            get_ldap_attr = lambda k: ldap_attrs.get(settings.get(k), [''])[0]

            # old attrs fetched from Kallithea database
            admin = getattr(userobj, 'admin', False)
            email = getattr(userobj, 'email', '')
            firstname = getattr(userobj, 'firstname', '')
            lastname = getattr(userobj, 'lastname', '')

            user_data = {
                'username': username,
                'firstname': safe_unicode(get_ldap_attr('attr_firstname') or firstname),
                'lastname': safe_unicode(get_ldap_attr('attr_lastname') or lastname),
                'groups': [],
                'email': get_ldap_attr('attr_email') or email,
                'admin': admin,
                'extern_name': user_dn,
            }
            log.info('user %s authenticated correctly', user_data['username'])
            return user_data

        except LdapUsernameError:
            log.info('Error authenticating %s with LDAP: User not found', username)
        except LdapPasswordError:
            log.info('Error authenticating %s with LDAP: Password error', username)
        except LdapImportError:
            log.error('Error authenticating %s with LDAP: LDAP not available', username)
        return None

    def get_managed_fields(self):
        return ['username', 'firstname', 'lastname', 'email', 'password']
