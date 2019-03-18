"""
{ item_description }
"""
# import sys
# import urllib
import json
from typing import Union
from datetime import datetime
import requests
# import pathlib
import urllib3

class Api:
    """
    @brief      Class for api connection to an IPA server.
    """

    def __init__(
            self,
            host: type=str,
            username: type=str,
            password: type=str,
            port: int=443,
            protocol: str='https',
            verify_ssl: bool=True,
            verify_method: Union[bool, str]=True,
            verify_warnings: bool=True,
            version: str='2.228',
            dryrun: bool=False
    ):
        """
        @brief The initiator of the pyfreeipa.Api class

        @param self This object
        @param host The address of the IPA server
        @param username The username of the IPA user to connect to the IPA server
        @param password The password for the IPA user
        @param port The port to connect to (Default: 443)
        @param protocol The protocol to connect with (Default: https)
        @param verify_ssl If True then the TLS/SSL connection will verified as being secure and has valid certificates. (Default: True)
        @param verify_method Can be a True, False, or a string pointing to a certificate or directory holding certificaates. (Default: True)
        @param verify_warnings If True then TLS/SSL warnings will be emitted to stderr. (Default: True)
        @param version Used to over-ride the default IPA API version string. (Default: 2.228)
        @param dryrun If set to True this will stop any requests from making changes to the IPA directory (Default: False)
        """

        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._protocol = protocol
        self._verify_ssl = verify_ssl
        self._verify_method = verify_method
        self._verify_warnings = verify_warnings
        self._version = version
        self._dryrun = dryrun

        self.warnings = []

        if not self._verify_warnings:
            reason = (
                'Verifying TLS connection to %s disabled.' %
                self._host
            )
            self.warnings.append(reason)

        self._baseurl = (
            "%s://%s/ipa" %
            (
                self._protocol,
                self._host
            )
        )

        self._sessionurl = "%s/session/json" % self._baseurl
        self._loginurl = "%s/session/login_password" % self._baseurl

        if not self._verify_warnings:
            reason = (
                "TLS warnings from %s disabled" %
                self._host
            )
            self.warnings.append(reason)
            urllib3.disable_warnings()

        self._session = requests.Session()
        self._session.url = self._baseurl
        self._session.verify = self._verify_ssl
        self._session.headers = {
            'Referer': self._baseurl,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.login()

    def get(
            self,
            *dargs,
            **kwargs
    ):
        """
        @brief This exposes a raw get method for the session
        """
        response = self._session.get(
            *dargs,
            **kwargs
        )
        return response

    def post(
            self,
            *dargs,
            **kwargs
    ):
        """
        @brief This exposes a raw post method for the internal session
        """
        response = self._session.post(
            *dargs,
            **kwargs
        )
        return response

    def put(
            self,
            *dargs,
            **kwargs
    ):
        """
        @brief This exposes a raw put method for the internal session
        """
        response = self._session.put(
            *dargs,
            **kwargs
        )
        return response

    def request(
            self,
            method: str,
            args=None,
            params=None
    ):
        """
        @brief This cleans up the args and parameters posts the and handles
        the request and returns the response

        @param self This object
        @param method The FreeIPA API method to request
        @param args A list of arguments to be passed to the method request
        @param params A dictionary of parameters to be passed to the method request

        @return a requests.Response object
        """
        if args:
            if not isinstance(args, list):
                args = [args]
        else:
            args = []

        if not params:
            params = {}

        if self._version:
            params.setdefault('version', self._version)

        data = {
            'id': 0,
            'method': method,
            'params': [args, params]
        }

        response = self.post(
            self._sessionurl,
            data=json.dumps(data)
        )

        return response

    def preprequest(
            self,
            method: str,
            args=None,
            params=None
    ):
        """
        @brief This cleans up the args and parameters posts the and creates a prepared reques from the internal sessions object

        @param self This object
        @param method The FreeIPA API method to request
        @param args A list of arguments to be passed to the method request
        @param params A dictionary of parameters to be passed to the method request

        @return a requests.Response object
        """
        if args:
            if not isinstance(args, list):
                args = [args]
        else:
            args = []

        if not params:
            params = {}

        if self._version:
            params.setdefault('version', self._version)

        data = {
            'id': 0,
            'method': method,
            'params': [args, params]
        }

        request = requests.Request(
            'POST',
            self._sessionurl,
            data=json.dumps(data)
        )

        return self._session.prepare_request(request)

    def clearwarnings(self):
        """
        @brief      Retrieve and clear the warning array

        @param      self  The object

        @return     the warnings array before it was cleared
        """
        warnings = self.warnings
        self.warnings = []
        return warnings

# All definitions from this point are IPA API commands
# Two sections Read and Write, with methods in alphabetical order

# Read methods that make no change to the directory and should work in

    def login(self):
        """
        @brief      Returns the response from the login command

        @param      self  The object

        @return     the requests.Response from the login request
        """
        logindata = {
            'user': self._username,
            'password': self._password
        }

        loginheaders = {
            'referer': self._loginurl,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        response = self.post(
            self._loginurl,
            data=logindata,
            headers=loginheaders
        )

        return response

    def otptoken_find(
            self,
            searchstring: Union[str, None]=None,
            uniqueid: Union[str, None]=None,
            owner: Union[str, None]=None,
            no_members: Union[bool, None]=None,
            allattrs: Union[bool, None]=None,
            raw: Union[bool, None]=None
    ):
        """
        @brief Partial implementation the otptoken_show request, only searches by parameters below

        @param self The object
        @param uniqueid, the unique identifier (`iparokenuniqueid`) attribute of the token to find
        @param owner, the owner (`iparokenowner`) attribute of the token to find
        @param no_members, if true this suppresses processing of membershib attributes
        @param all, retrieves all attributes
        @param raw, returns the raw response, only changes output format

        @return the request.Response from the otpoken_show request
        """

        method = 'otptoken_find'

        args = None

        if searchstring:
            args = searchstring

        params = {}

        if uniqueid is not None:
            params['ipatokenuniqueid'] = uniqueid

        if owner is not None:
            params['ipatokenowner'] = owner

        if no_members is not None:
            params['no_members'] = no_members

        if allattrs is not None:
            params['all'] = allattrs

        if raw is not None:
            params['raw'] = raw

        return self.request(
            method,
            args=args,
            params=params
        )

    def otptoken_show(
            self,
            uniqueid: str,
            no_members: Union[bool, None]=None,
            allattrs: Union[bool, None]=None,
            raw: Union[bool, None]=None
    ):
        """
        @brief Complete implementation the otptoken_show request

        @param self The object
        @param uniqueid, the unique identifier (`iparokenuniqueid`) attribute of the token to show
        @param no_members, if true this suppresses processing of membershib attributes
        @param all, retrieves all attributes
        @param raw, returns the raw response, only changes output format

        @return the request.Response from the otpoken_show request
        """

        method = 'otptoken_show'

        args = uniqueid

        params = {}

        if no_members is not None:
            params['no_members'] = no_members

        if allattrs is not None:
            params['all'] = allattrs

        if raw is not None:
            params['raw'] = raw

        return self.request(
            method,
            args=args,
            params=params
        )

    def ping(self):
        """
        @brief      Returns the response from the ping command

        @param      self  The object

        @return     the requests.Response from the ping request
        """
        return self.request('ping')

    def user_find(
            self,
            searchstring: Union[str, None]=None,
            uid: Union[str, None]=None,
            uidnumber: Union[int, None]=None,
            in_group: Union[str, list, None]=None,
            mail: Union[str, list, None]=None,
            rights: Union[bool, None]=None,
            allattrs: Union[bool, None]=None,
            raw: Union[bool, None]=None
    ):
        """
        @brief      A partial implementation of the user_find request

        @param      self  The object

        @param      uid of the user to be shown

        @param      rights, if true, displays the access rights of this user

        @param      all, retrieves all attributes

        @param      raw, returns the raw response, only changes output format

        @return     the requests.Response from the ping request
        """

        method = 'user_find'

        args = None

        if searchstring:
            args = searchstring

        params = {}

        if uid is not None:
            params['uid'] = uid

        if uidnumber is not None:
            params['uidnumber'] = uidnumber

        if in_group is not None:
            params['in_group'] = in_group

        if mail is not None:
            params['mail'] = mail

        if rights is not None:
            params['rights'] = rights

        if allattrs is not None:
            params['all'] = allattrs

        if raw is not None:
            params['raw'] = raw

        return self.request(
            method,
            args=args,
            params=params
        )

    def user_show(
            self,
            uid: str,
            rights: Union[bool, None]=None,
            allattrs: Union[bool, None]=None,
            raw: Union[bool, None]=None
    ):
        """
        @brief      A complete implementation of the user_show command

        @param      self  The object

        @param      uid of the user to be shown

        @param      rights, if true, displays the access rights of this user

        @param      all, retrieves all attributes

        @param      raw, returns the raw response, only changes output format

        @return     the requests.Response from the ping request
        """

        method = 'user_show'

        args = uid

        params = {}

        if rights is not None:
            params['rights'] = rights

        if allattrs is not None:
            params['all'] = allattrs

        if raw is not None:
            params['raw'] = raw

        return self.request(
            method,
            args=args,
            params=params
        )

    def whoami(self):
        """
        @brief      Returns the response from the whoami command

        @param      self  The object

        @return     the requests.Response from the whoami request
        """
        return self.request('whoami')

# Write methods that may cause changes to the directory
# These methods MUST require dryrun to be false to write changes

    def otptoken_add(
            self,
            # Arguments
            uniqueid: str,
            # Options
            otptype: Union[str, None]=None,
            description: Union[str, None]=None,
            owner: Union[str, None]=None,
            disabled: Union[bool, None]=None,
            notbefore: Union[datetime, None]=None,
            notafter: Union[datetime, None]=None,
            vendor: Union[str, None]=None,
            model: Union[str, None]=None,
            serial: Union[str, None]=None,
            otpkey: Union[str, None]=None,
            otpalgorithm: Union[str, None]=None,
            otpdigits: Union[int, None]=None,
            otpclockoffset: Union[int, None]=None,
            otptimestep: Union[int, None]=None,
            otpcounter: Union[int, None]=None,
            no_qrcode: Union[bool, None]=None,
            no_members: Union[bool, None]=None,
            otpsetattr: Union[list, None]=None,
            addattr: Union[list, None]=None,
            # Custom
            managedby: Union[list, None]=None
    ):

        method = 'otptoken_add'

        args = uniqueid

        params = {}

        # These options need some checking before submitting a request
        typevalues = ['totp', 'hotp', 'TOTP', 'HOTP']
        if otptype is not None:
            if otptype in typevalues:
                params['type'] = otptype
            else:
                raise ValueError(
                    "otptoken_add: otptype must be one of %r" % typevalues
                )

        algovalues = ['sha1', 'sha256', 'sha384', 'sha512']
        if otpalgorithm is not None:
            if otpalgorithm.lower() in algovalues:
                params['ipatokenotpalgorithm'] = otpalgorithm.lower()
            else:
                raise ValueError(
                    "otptoken_add: otpalgorithm must be one of %r" % typevalues
                )

        # These options just need to be mapped to request parameters
        if description is not None:
            params['description'] = description

        if owner is not None:
            params['ipatokenowner'] = owner

        if disabled is not None:
            params['ipatokendisabled'] = disabled

        if notafter is not None:
            params['ipatokennotafter'] = notafter

        if notbefore is not None:
            params['ipatokennotbefore'] = notbefore

        if vendor is not None:
            params['ipatokenvendor'] = vendor

        if model is not None:
            params['ipatokenmodel'] = model

        if serial is not None:
            params['ipatokenserial'] = serial

        if otpkey is not None:
            params['ipatokenotpkey'] = otpkey

        if otpdigits is not None:
            params['ipatokenotpdigits'] = otpdigits

        if otpclockoffset is not None:
            params['ipatokentotpclockoffset'] = otpclockoffset

        if otptimestep is not None:
            params['ipatokentotptimestep'] = otptimestep

        if otpcounter is not None:
            params['ipatokenhotpcounter'] = otpcounter

        if no_qrcode is not None:
            params['no_qrcode'] = no_qrcode

        if no_members is not None:
            params['no_members'] = no_members

        if otpsetattr is not None:
            params['setattr'] = otpsetattr

        if addattr is not None:
            params['addattr'] = addattr
        # Custom
        if managedby is not None:
            print("I'm special")

        prepared = self.preprequest(
            method,
            args=args,
            params=params
        )

        if not self._dryrun:
            response = self._session.send(prepared)
        else:
            response = prepared

        return response

    def otptoken_add_managedby(
            self,
            # Arguments
            uniqueid: str,
            user: Union[list, str],
            no_members: Union[bool, None]=None,
            allattrs: Union[bool, None]=None,
            raw: Union[bool, None]=None
    ):
        """
        @brief adds a user to the managedBy attributes

        @return the response from the otptoken_add_managedby request, unless dry run where it returns the prepared response
        """

        method = 'otptoken_add_managedby'

        args = uniqueid

        if not isinstance(user, list):
            user = [user]

        params = {
            'user': user
        }

        if no_members is not None:
            params['no_members'] = no_members

        if allattrs is not None:
            params['all'] = allattrs

        if raw is not None:
            params['raw'] = raw

        prepared = self.preprequest(
            method,
            args=args,
            params=params
        )

        if not self._dryrun:
            response = self._session.send(prepared)
        else:
            response = prepared

        return response

    def otptoken_remove_managedby(
            self,
            # Arguments
            uniqueid: str,
            user: Union[list, str],
            no_members: Union[bool, None]=None,
            allattrs: Union[bool, None]=None,
            raw: Union[bool, None]=None
    ):
        """
        @brief removes a user to the managedBy attributes

        @return the response from the otptoken_add_managedby request, unless dry run where it returns the prepared response
        """

        method = 'otptoken_remove_managedby'

        args = uniqueid

        if not isinstance(user, list):
            user = [user]

        params = {
            'user': user
        }

        if no_members is not None:
            params['no_members'] = no_members

        if allattrs is not None:
            params['all'] = allattrs

        if raw is not None:
            params['raw'] = raw

        prepared = self.preprequest(
            method,
            args=args,
            params=params
        )

        if not self._dryrun:
            response = self._session.send(prepared)
        else:
            response = prepared

        return response

# The next methods produce objects, or lists or objects
# These are intended for simple operations that don't require
# full feedback from the response objecs
# e.g. won't say why a request found nothing

    def otptoken(
            self,
            uniqueid: str
    ):
        """
        @brief      { function_description }

        @param      self      The object
        @param      uniqueid  The uniqueid of he token to be returned

        @return     { description_of_the_return_value }
        """

        response = self.otptoken_show(uniqueid, allattrs=True)

        if response.json()['result']:
            return response.json()['result']['result']
        else:
            return None

    def otptokens(
            self,
            searchstring: Union[str, None]=None,
            uniqueid: Union[str, None]=None,
            owner: Union[str, None]=None
    ):
        """
        @brief      { function_description }

        @param      self          The object
        @param      searchstring  The searchstring used on any otptoken attribute
        @param      uniqueid      substring used to match otptoken uniqueid
        @param      owner         search for tokens owned but specified user

        @return     { description_of_the_return_value }
        """

        response = self.otptoken_find(
            searchstring=searchstring,
            uniqueid=uniqueid,
            owner=owner,
            allattrs=True
        )

        if response.json()['result']:
            return response.json()['result']['result']
        else:
            return []

    def user(
            self,
            uid: str
    ):
        """
        @brief      { function_description }

        @param      self  The object
        @param      uid   The uid of the user to return

        @return     the user account as a dictionary
        """

        response = self.user_show(uid, allattrs=True)

        if response.json()['result']:
            return response.json()['result']['result']
        else:
            return None

    def users(
            self,
            searchstring: Union[str, None]=None,
            uid: Union[str, None]=None,
            uidnumber: Union[int, None]=None,
            in_group: Union[str, list, None]=None,
            mail: Union[str, list, None]=None,
    ):
        """
        @brief      { function_description }

        @param      self          The object
        @param      searchstring  The searchstring used on any otptoken attribute
        @param      uniqueid      substring used to match otptoken uniqueid
        @param      owner         search for tokens owned but specified user

        @return     { description_of_the_return_value }
        """

        response = self.user_find(
            searchstring=searchstring,
            uid=uid,
            uidnumber=uidnumber,
            in_group=in_group,
            mail=mail,
            allattrs=True
        )

        if response.json()['result']:
            return response.json()['result']['result']
        else:
            return []
