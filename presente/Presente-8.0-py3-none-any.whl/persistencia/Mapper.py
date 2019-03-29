from persistencia.Connection import Connection
from logica.Student          import Student
from logica.Date             import Date
from logica.Usefull          import Usefull
from datetime                import date, datetime
class Mapper:
    def __init__(self,student):
        self.__connection  = Connection()
        self.__student     = student

    def save(self):
        today = date.today()
        self.__connection.update(""" INSERT INTO alumnos(nombre,apellido,cedula,telefono,emailPadre,emailMadre,fechaRegistro)
                                     VALUES(?,?,?,?,?,?,?);""",(self.__student.getFirstName(),self.__student.getLastName(),self.__student.getIdentification(),self.__student.getPhone(),self.__student.getFatherMail(),self.__student.getMotherMail(),today))

    def update(self):
        self.__connection.update(""" UPDATE alumnos 
                                     SET 
                                         nombre     = ?,
                                         apellido   = ?,
                                         telefono   = ?,
                                         emailPadre = ?,
                                         emailMadre = ?
                                      WHERE cedula     = ?;""",(self.__student.getFirstName(),self.__student.getLastName(),self.__student.getPhone(),self.__student.getFatherMail(),self.__student.getMotherMail(),self.__student.getIdentification()))

    def totalClass(self,fecha):
        resultado=self.__connection.scalar(""" SELECT  COUNT(*) 
                                               FROM    clases
                                               WHERE fecha>=?""",([fecha]))

        return int(resultado[0]) 
    
    def totalStatistics(self,identification):
        resultado=self.__connection.scalar(""" SELECT  COUNT(*) 
                                               FROM    presente
                                               WHERE   cedula=?""",([identification]))
        present=int(resultado[0])
        resultado=self.__connection.scalar(""" SELECT  fechaRegistro 
                                               FROM    alumnos
                                               WHERE   cedula = ?""",([identification]))
        
        date= resultado[0]
        
        
        
        totalClass=self.totalClass(date)
        averagePresent=0
        if totalClass > 0:
            averagePresent=((present*100)/totalClass)
        skipped=totalClass-present
        if present==0:
            skipped=0
        return [present,skipped,averagePresent]
    
    def delete(self,identification):
        self.__connection.update(""" DELETE 
                                     FROM alumnos
                                     WHERE cedula = ?;""",([identification]))


    def exists(self,identification):
        resultado=self.__connection.scalar(""" SELECT  COUNT(*) AS cantidad 
                                               FROM    alumnos
                                               WHERE   cedula = ? """,([identification]))
        
        return int(resultado[0])==1 
    def listStudent(self):
        students=self.__connection.query(""" SELECT  *
                                             FROM    alumnos""",())
        list=[]
        for field in students:
            student=self.createStudent(field)
            list.append(student)
        return list 

    def opening (self,fecha):
        self.__connection.update(""" INSERT INTO clases(fecha,cierre)
                                     VALUES(?,NULL)""",[fecha])
    
    def present(self,cedula,fecha):
           
            self.__connection.update(""" INSERT INTO presente(fecha,cedula)
                                         VALUES(?,?);""",(fecha,cedula))
            
    
    def closing(self,fechaInicial,fecha):
        self.__connection.update(""" UPDATE clases
                                     SET    cierre= ?
                                     WHERE  fecha = ?""",[fecha,fechaInicial])

    def presentToday(self,fecha):
        listStudent=self.__connection.query("""      SELECT  alumnos.* 
                                                     FROM    alumnos INNER JOIN presente ON alumnos.cedula=presente.cedula 
                                                     WHERE   fecha=?
                                                     ORDER BY apellido,nombre""",([fecha]))

        listRespuest=[]
        for field in listStudent:
            student=self.createStudent(field)
            listRespuest.append(student)
        return listRespuest 
    
    def isWanting(self):
        resultado=self.__connection.scalar("""SELECT  COUNT(*) AS cantidad 
                                              FROM    alumnos
                                              WHERE   alumnos.cedula NOT IN (SELECT presente.cedula
                                                                             FROM presente
                                                                             WHERE  fecha=?)""",[Usefull.today()])
        
        return int(resultado[0])>0
    
    def wanting(self,fecha):
        listStudent=self.__connection.query("""      SELECT  * 
                                                     FROM    alumnos
                                                     WHERE   alumnos.cedula NOT IN (SELECT presente.cedula
                                                                                    FROM presente
                                                                                    WHERE  fecha=?)
                                                     ORDER BY apellido,nombre""",[fecha])

        result=Date()
        result.setDate(fecha)
        for field in listStudent:
            student=self.createStudent(field)
            result.add(student)

        return result

    def find(self,identificator):
        line=self.__connection.scalar("""     SELECT  * 
                                              FROM    alumnos
                                              WHERE   alumnos.cedula =?""",[identificator])
        student=self.createStudent(line)

        return student
    
    def createStudent(self,line):
        if line is None:
            return None
        else:
            statistics=self.totalStatistics(line[0])
            student= Student(line[1],line[2],line[0],line[3],line[5],line[4])
            student.generateStatistics(statistics)
            return student

    def isOpening(self,date):
        resultado=self.__connection.scalar(""" SELECT COUNT(*)
                                               FROM clases
                                               WHERE fecha=?""",[date])
        return int(resultado[0])==1 
    
    def isPresent(self,identification,date):
        resultado=self.__connection.scalar(""" SELECT  COUNT(*) AS cantidad 
                                               FROM    presente
                                               WHERE   cedula = ? AND fecha=?""",([identification,date]))
        
        return int(resultado[0])==1
    
    def listPresent(self,desde,hasta):
        listStudent=self.__connection.query("""      SELECT  alumnos.* 
                                                     FROM    alumnos INNER JOIN presente ON alumnos.cedula=presente.cedula 
                                                     WHERE   fecha=?
                                                     ORDER BY apellido,nombre""",([fecha]))

        listRespuest=[]
        for field in listStudent:
            student=self.createStudent(field)
            listRespuest.append(student)
        return listRespuest 
    
    
