import xmltodict


class Response:
    def __init__( self, response ):
        self._response = response

    @property
    def body( self ):
        return self._response

    @property
    def native( self ):
        return self.body


class Response_xml( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            self._native = xmltodict.parse( self.body )
            return self._native
