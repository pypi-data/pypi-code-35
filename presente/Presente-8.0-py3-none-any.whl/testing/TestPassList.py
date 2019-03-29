import unittest
import time
from logica.Date              import Date
from logica.Student           import Student
from logica.System            import System
from persistencia.MapperTest  import MapperTest

class TestPassList(unittest.TestCase):

    def setUp(self):
        print("Preparando informacion Test Fecha")
        MapperTest()

        student1=Student('Carlos','Sanchez',123,'099','carlosalesanchez@gmail.com','carlosalesanchez@gmail.com')
        student2=Student('Franco','sssssss',321,'094','franco@gmail.com'          ,'franco@gmail.com')
        student3=Student('Sofia' ,'ddddddd',222,'093','sofia@gmail.com'           ,'sofia@gmail.com')
        student4=Student('Mai'   ,'fffffff',223,'097','mai@gmail.com'             ,'mai@gmail.com')

        self.listStudents=[student1,student2,student3,student4]
        for student in self.listStudents:
            System.save(student) 

    def testMissAll(self):
        print("Test Falto todos")
        respuesta=Date()
        respuesta.add(self.listStudents[0])
        respuesta.add(self.listStudents[2])
        respuesta.add(self.listStudents[3])
        respuesta.add(self.listStudents[1])
        fecha=time.strftime("%d/%m/%y")
        
        System.opening(fecha)
        System.closing(fecha,fecha)
        fechaGenerado=System.wanting(fecha)

        self.assertEqual(fechaGenerado,respuesta ,"Prueba que faltaron todos")

    def testMiss(self):
        respuesta=Date()
        respuesta.add(self.listStudents[0])
        respuesta.add(self.listStudents[2])
        fecha=time.strftime("%d/%m/%y")
        
        System.opening(fecha)
        System.present(321,fecha)
        System.present(223,fecha)
        System.closing(fecha,fecha)
        fechaGenerado=System.wanting(fecha)

        self.assertEqual(fechaGenerado,respuesta ,"Prueba que faltaron dos")

    def testMissNone(self):
        print("Test Falto Ninguno")
        respuesta=Date()
        fecha=time.strftime("%d/%m/%y")

        System.opening(fecha)
        
        System.present(321,fecha)
        System.present(223,fecha)
        System.present(123,fecha)
        System.present(222,fecha)
        System.closing(fecha,fecha)
        fechaGenerado=System.wanting(fecha)
        self.assertEqual(fechaGenerado,respuesta ,"Prueba que faltaron ninguno")    

    def tearDown(self):
        mapper=MapperTest()
        mapper.clear()
        
if __name__ == '__main__':
    unittest.main()