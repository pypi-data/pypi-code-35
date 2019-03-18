from datetime import datetime


class Timekeeper:
    def __init__( self, arguments=None, message=None, used_a_factory=None ):
        self.start = None
        self.end = None
        self.raw_result = None
        self.result = None
        self.arguments = arguments
        self.message = message
        self.used_a_factory = bool( used_a_factory )

    @property
    def delta( self ):
        return self.end - self.start

    def __enter__( self ):
        self.start = datetime.utcnow()

    def __exit__( self, exc_type, exc_value, traceback ):
        self.end = datetime.utcnow()
