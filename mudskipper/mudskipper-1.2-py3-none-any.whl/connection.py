from urllib.parse import urljoin
from zeep import Client
from mudskipper.endpoint import Endpoint


__all__ = [ 'Connections_http', 'Connections_soap' ]


class Connections_base:
    def __init__( self ):
        self._kwargs = {}
        self._connections = {}

    def configure( self, **kw ):
        """
        remplace all the connections

        Parameters
        ==========
        kw: dict
            the key is the name of the connection and the value is the
            dictiontary with all the connection data
        """
        self._connections = kw

    def add( self, name, connection ):
        """
        add a new connection

        Parameters
        ==========
        name: str
            name of the new connection
        connection: dict
            all the info for the connection
        """
        self._connections[ name ] = connection

    def get( self, alias='default' ):
        """
        retrive the connection

        Parameters
        ==========
        alias: str
            name of the connection want to retrive

        Returns
        =======
            dict
        """
        if not isinstance( alias, str ):
            raise TypeError(
                "unexpected type '{}' expected '{}'" .format(
                    type( alias ), str ) )

        try:
            return self._connections[ alias ]
        except KeyError:
            raise KeyError(
                "there is no connection with name {}".format( alias ) )

    def __getitem__( self, name ):
        return self.get( name )

    def __setitem__( self, name ):
        return self.add( name )


class Connections_http( Connections_base ):
    def build_endpoint( self, alias='default', url=None, endpoint_class=None ):
        """
        build a endpoint

        Parameters
        ==========
        url: str
            string is going to be joined to the host url

        Returns
        =======
        py:class`mudskipper.endpoint.Endpoint`
        """
        connection = self[ alias ]
        if url is None:
            url = connection[ 'host' ]
        else:
            url = urljoin( connection[ 'host' ], url )
        if endpoint_class is None:
            endpoint_class = Endpoint
        return endpoint_class( url, proxy=connection.get( 'proxy' ) )


class Connections_soap( Connections_base ):
    def build_zeep_client(self, alias='default'):

        connection = self[alias]
        wsdl = connection['wsdl']
        proxies = connection.get('proxies', None)
        client = Client(wsdl)

        if proxies:
            client.transport.session.proxies = proxies

        return client


Connections = Connections_http
