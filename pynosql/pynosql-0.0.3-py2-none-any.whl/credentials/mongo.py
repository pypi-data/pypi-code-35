import ssl
from pynosql.credentials.base_credentials import \
    BaseCredentials, InvalidCredentials


class MongoDBSSLCredentials(BaseCredentials):
    """ MongoDB SSL Credentials """

    SSL = ssl

    def __init__(self, ssl_cert_file, ssl_cert_reqs, ssl_ca_certs):
        """ MongoDB SSL Credentials Object

        :param ssl_cert_file: str path to certificate file
        :param ssl_cert_reqs: str ssl requirements
        :param ssl_ca_certs: str path to ca certificate
        """
        self.cert_file = ssl_cert_file
        self.cert_reqs = ssl_cert_reqs
        self.ca_certs = ssl_ca_certs
        self.check_credentials()

    @property
    def certificate_file(self):
        """ Certificate file path

            '/path/to/certificate'

        :return: str certificate path
        """
        return self.cert_file

    @property
    def certificate_requirements(self):
        """ SSL certificate requirements

        :return: object certificate requirements
        """
        return self.cert_reqs

    @property
    def ca_certificates(self):
        """ CA certificate path

            '/path/to/ca/certificates/'

        :return: str ca certificate path
        """
        return self.ca_certs

    def check_credentials(self):
        """ Check if credentials are not None

        :raises: InvalidCredentials
        """
        if not self.certificate_file or \
                not self.certificate_requirements or not self.ca_certificates:
            raise InvalidCredentials('Credentials must contain a value.')


class MongoDBCredentials(BaseCredentials):
    """ MongoDB Credentials Provider """

    def __init__(self, username=None, password=None,
                 source=None, mechanism=None, ssl_obj=None):
        """ MongoDB Credentials Provider

        :param username: str username
        :param password: str password
        :param source: str credentials source
        :param mechanism: str credentials mechanism
        :param ssl_obj: obj MongoDBSSLCredentials
        """
        self.auth_username = username
        self.auth_password = password
        self.auth_source = source
        self.auth_mechanism = mechanism
        self.ssl_enabled = False
        self.auth_ssl = ssl_obj
        self.check_credentials()

    @property
    def username(self):
        """ Username property

        :return: str username
        """
        return self.auth_username

    @property
    def password(self):
        """ Password property

        :return: str password
        """
        return self.auth_password

    @property
    def source(self):
        """ Authentication source property

        :return: str source
        """
        return self.auth_source

    @property
    def mechanism(self):
        """ Authentication mechanism property

        :return: str mechanism
        """
        return self.auth_mechanism

    @property
    def is_ssl_enabled(self):
        """ Boolean if SSL is enabled for credentials

        :return: bool ssl credentials
        """
        return self.ssl_enabled

    @property
    def ssl_detail(self):
        """ SSL property

        :return: str ssl
        """
        return self.auth_ssl

    def check_credentials(self):
        """ Check if ssl credentials are valid instance

        :return: None
        """
        if self.ssl_detail:
            if not isinstance(self.ssl_detail, MongoDBSSLCredentials):
                raise InvalidCredentials(
                    'SSL is not an instance of MongoDBSSLCredentials.')
            self.ssl_enabled = True
