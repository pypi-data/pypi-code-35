from persistencia.Connection  import Connection
from logica.Student           import Student

class MapperTest:
    def __init__(self):
        self.__connection = Connection()
        self.clear()

    def clear(self):
        self.__connection.update(""" DELETE
                                            FROM alumnos""",())
        self.__connection.update(""" DELETE
                                            FROM clases""",())
        self.__connection.update(""" DELETE
                                            FROM presente""",())
        
