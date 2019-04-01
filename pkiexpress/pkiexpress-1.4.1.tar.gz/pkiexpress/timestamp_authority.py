"""

Module that contains the timestamp authority class.

"""


class TimestampAuthority(object):
    """

    Class that contains information of the timestamp authority used to perform
    a signature with timestamp.

    """
    NONE = 0
    BASIC_AUTH = 1
    SSL = 2
    OAUTH_TOKEN = 3

    def __init__(self, url):
        self.__url = url
        self.__token = None
        self.__ssl_thumbprint = None
        self.__basic_auth = None
        self.__auth_type = TimestampAuthority.NONE
        self.__request_timeout = 15

    def set_oauth_token_authentication(self, token):
        """

        Sets the authentication type to use OAuth token.
        :param token: The OAuth token.

        """
        self.__token = token
        self.__auth_type = TimestampAuthority.OAUTH_TOKEN

    def set_basic_authentication(self, username, password):
        """

        Sets the authentication type to use basic authentication with 'username'
        and 'password'.
        :param username: The 'username' parameter.
        :param password: The 'password' parameter.

        """
        self.__basic_auth = "%s:%s" % (username, password)
        self.__auth_type = TimestampAuthority.BASIC_AUTH

    def set_ssl_authentication(self, ssl_thumbprint):
        """

        Sets the authentication type to use mutual SSL authentication.
        :param ssl_thumbprint: The certificate's thumbprint used on mutual SSL
        authentication.

        """
        self.__ssl_thumbprint = ssl_thumbprint
        self.__auth_type = TimestampAuthority.SSL

    @property
    def url(self):
        """

        Property for the URL of the timestamp authority.
        :return: The URl of the timestamp authority.

        """
        return self.__url

    @property
    def token(self):
        """

        Property for the OAuth token used on OAuth authentication.
        :return: The OAuth token.

        """
        return self.__token

    @property
    def ssl_thumbprint(self):
        """

        Property for the certificate's thumbprint for the mutual SSl
        authentication.
        :return: The certificate's thumbprint.

        """
        return self.__ssl_thumbprint

    @property
    def basic_auth(self):
        """

        Property for the basic authentication parameters on the format
        'username:password'.
        :return: The basic authentication parameters.

        """
        return self.__basic_auth

    # region "request_timeout" accessors

    @property
    def request_timeout(self):
        return self.__get_request_timeout()

    def __get_request_timeout(self):
        return self.__request_timeout

    @request_timeout.setter
    def request_timeout(self, value):
        self.__set_request_timeout(value)

    def __set_request_timeout(self, value):
        if value is None:
            raise Exception('The provided "request_timeout" is not valid')
        self.__request_timeout = value

    # endregion

    def add_cmd_arguments(self, args, version_manager):
        """

        Adds the CMD arguments to the command related to the timestamp
        authority authentication.
        :param args: The CMD arguments.
        :param version_manager: Version manager to inform the required version.

        """
        args.append('--tsa-url')
        args.append(self.__url)

        # User choice SSL authentication.
        if self.__auth_type is TimestampAuthority.NONE:
            pass
        elif self.__auth_type is TimestampAuthority.BASIC_AUTH:
            args.append('--tsa-basic-auth')
            args.append(self.__basic_auth)
        elif self.__auth_type is TimestampAuthority.SSL:
            args.append('--tsa-ssl-thumbprint')
            args.append(self.__ssl_thumbprint)
        elif self.__auth_type is TimestampAuthority.OAUTH_TOKEN:
            args.append('--tsa-token')
            args.append(self.__token)
        else:
            raise Exception('Unknown authentication type of the timestamp'
                            'authority')

        if self.__request_timeout:
            args.append('--ts-request-timeout')
            args.append(str(self.__request_timeout))
            # This option can only be used on versions greater than 1.12.2 of
            # the PKI Express
            version_manager.require_version('1.12.2')


__all__ = ['TimestampAuthority']
