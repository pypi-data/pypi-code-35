import time

class ClassRoom:
    def __init__(self):
        self.__date     = time.strftime("%d/%m/%y")
        self.__present  = []
        self.__waiting  = []

    def getDate(self):
        return self.__date
    
    def setDate(self,date):
        self.__date=date
             
    def getPresentList(self):
        return self.__presentList

    def getWitingList(self):
        return self.__waiting

    def empty(self):
        return len(self.__studentsList)==0
    
    def existsStudent(self,student):
        return student in self.__studentsList

    def addPresent(self,student):
        self.__present.append(student)
    
    def addWaiting(self,student):
        self.__waiting.append(student)
    
    def __repr__(self):

        return " date : {} Listado de students {}".format( self.__date,self.__studentsList)

    def __eq__(self, other): 
        
        meet=True
        if self.__date == other.getDate():
            count = len(other.getStudentsList())
            if len(self.__studentsList)==count:
                otherListing = other.getStudentsList()
                for i in range(0,count):
                    anotherStudent  = otherListing[i]
                    student      = self.__studentsList[i]
                    if student!=anotherStudent:                        
                        meet=False
            else:                
                meet=False
        else:           
            meet=False
        return meet
