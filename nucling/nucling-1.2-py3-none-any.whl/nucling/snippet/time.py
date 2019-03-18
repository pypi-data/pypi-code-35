from datetime import datetime


class Timekeeper:
    def __init__( self ):
        self.start = None
        self.end = None

    @property
    def delta( self ):
        return self.end - self.start

    def __enter__( self ):
        self.start = datetime.utcnow()

    def __exit__( self, exc_type, exc_value, traceback ):
        self.end = datetime.utcnow()
