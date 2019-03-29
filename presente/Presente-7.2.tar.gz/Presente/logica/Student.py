
class Student:
    
    def __init__(self, firstName,lastName,identification ,Phone,fatherMail,motherMail):
        """Constructor de Alumno"""
        self.__firstName       = firstName
        self.__lastName        = lastName
        self.__identification  = identification 
        self.__phone 	       = Phone
        self.__fatherMail	   = fatherMail
        self.__motherMail	   = motherMail
        self.__skipped         = 0
        self.__present         = 0
        self.__total           = 0
        
    def getFirstName(self):
        return self.__firstName
    
    def setFirstName(self,FirstName):
        self.__firstName=FirstName
        
    def getLastName(self):
        return self.__lastName
    
    def setLastName(self,LastName):
        self.__lastName=LastName    
        
    def getIdentification (self):
        return self.__identification
    
    def setIdentification (self,identification ):
        self.__identification =identification 
        
    def getPhone(self):
        return self.__phone
    
    def setPhone(self,phone):
        self.__phone =phone   
        
    def getFatherMail(self):
        return self.__fatherMail
    
    def setFatherMail(self,fatherMail):
        self.__fatherMail=fatherMail

    def getMotherMail(self):
        return self.__motherMail
    
    def setMotherMail(self,motherMail):
        self.__motherMail=motherMail
    
    def getSkipped(self):
        return self.__skipped
    
    def setSkipped(self,skipped):
        self.__skipped=skipped
        
    def getPresent(self):
        return self.__present
    
    def setPresent(self,present):
        self.__present=present
    
    def getTotal(self):
        return self.__total
    
    def setTotal(self,total):
        self.__total=total
    def __repr__(self):

        return "{}-{}".format( self.getLastName(),self.getFirstName())


    def __eq__(self, other): 
        return int(self.__identification ) == int(other.getIdentification ())

    def __cmp__(self, other):
        return int(self.__identification ) - int(other.getIdentification ())
    
    def fullName(self):
        return self.__firstName+" "+self.__lastName
    
    def generateStatistics(self,statistics):
        self.__present=statistics[0]
        self.__skipped=statistics[1]
        self.__total  =statistics[2]