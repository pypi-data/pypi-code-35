from .connection import (
    Connections_base as Connections, Connections_http, Connections_soap
)


class Client_base:
    """
    base client for apis

    Arguments
    =========
    connection_name: str
        name of the connection to use
    _connections: dict
        dictionary with all the conections can use this client
    """
    def __init__( self, connection_name='default', _connections=None ):
        if _connections is None:
            self._connections = self.build_connection()
        else:
            self._connections = _connections
        self._default_connection_name = connection_name

    def using( self, name ):
        """
        create another client with diferent connection

        Parameters
        ==========
        name: str
            name of the connection
        """
        self._connections[ name ]
        return self.__class__( name, _connections=self._connections )

    def extract_connections( self ):
        """
        retrieve the connections of this client
        """
        return self._connections

    def get_connection( self ):
        """
        get the current connection
        """
        return self._connections.get( self._default_connection_name )

    def build_connection( self ):
        """
        build the class for manage connections
        """
        return Connections()


class Client_http( Client_base ):
    def build_connection( self ):
        return Connections_http()


class Client_soap( Client_base ):
    def build_connection( self ):
        return Connections_soap()


Client = Client_http
