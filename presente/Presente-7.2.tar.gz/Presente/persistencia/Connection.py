from variablesGlobales import CONFIG_BASE
import sqlite3

class Connection:
    
    def __init__(self):

        self.path=CONFIG_BASE
        self.connect()
        
    def connect(self):
        
        self.__connect= sqlite3.connect(self.path)
        cursor        = self.__connect.cursor()
        self.create(cursor)
    
    def create(self,cursor):
        cursor.execute("""  CREATE TABLE  IF NOT EXISTS alumnos 
                            (
                                    cedula 	       VARCHAR(8)      NOT NULL PRIMARY KEY,
                                    nombre 	       VARCHAR(11)  NOT NULL,
                                    apellido       VARCHAR(11)  NOT NULL,
                                    telefono       VARCHAR(15)  NOT NULL,
                                    emailMadre     VARCHAR(200)	NULL,
                                    emailPadre     VARCHAR(200) NULL,
                                    fechaRegistro  DATE         NULL
                            );""")

        cursor.execute(""" CREATE TABLE  IF NOT EXISTS clases
                            (
                                    fecha   DATE NOT NULL PRIMARY KEY,
                                    cierre	DATE NULL
                            );""")

        cursor.execute(""" CREATE TABLE  IF NOT EXISTS presente
                            (
                                    cedula	CHAR(8)  NOT NULL REFERENCES alumnos(cedula),
                                    fecha	DATE 	 NOT NULL REFERENCES clase(fecha  ),
                                    PRIMARY KEY(cedula,fecha)
                            );

                       """)
    def update(self,sql,parameters):
        cursor=self.__connect.cursor()
        cursor.execute(sql,parameters)
        self.__connect.commit()
        
    def query(self,sql,parameters):
        cursor=self.__connect.cursor()
        return cursor.execute(sql,parameters)
        
    def scalar(self,sql,parameters):
        cursor=self.__connect.cursor()
        cursor.execute(sql,parameters)
        return cursor.fetchone()
    
    def __del__(self):
        self.__connect.close()
