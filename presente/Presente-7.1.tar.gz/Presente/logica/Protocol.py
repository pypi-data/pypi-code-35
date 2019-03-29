from configparser         import ConfigParser
from variablesGlobales    import CONFIG_PATH

class Protocol:
     def __init__(self):
        config = ConfigParser()
        config.read(CONFIG_PATH)
        self.__user     = config.get("protocolo", "user")
        self.__password = config.get("protocolo", "password")
        self.__server   = config.get("protocolo", "SMTP")
        self.__port     = config.get("protocolo", "puerto")
    
     def getUser(self):
         return self.__user
     
     def setUser(self,user):
         self.__user=user

     def getPassword(self):
         return self.__password
     
     def setPassword(self,password):
         self.__password=password
    
     def getServer(self):
         return self.__server
     
     def setServer(self,server):
         self.__server=server

     def getPort(self):
         return self.__port
     
     def setPort(self,port):
         self.__port=port     