import unittest
from logica.Student           import Student
from logica.System            import System
from persistencia.MapperTest  import MapperTest

class TestList(unittest.TestCase):

    def setUp(self):
        print("Preparando inicio Test Lista")
        MapperTest()
        
        student1=Student('Carlos','Sanchez',123,'099','carlosalesanchez@gmail.com','carlosalesanchez@gmail.com')
        student2=Student('Franco','sssssss',321,'094','franco@gmail.com'          ,'franco@gmail.com')
        student3=Student('Sofia' ,'ddddddd',222,'093','sofia@gmail.com'           ,'sofia@gmail.com')
        student4=Student('Mai'   ,'fffffff',223,'097','mai@gmail.com'             ,'mai@gmail.com')

        self.listStudents=[student1,student2,student3,student4]
        for student in self.listStudents:
            System.save(student) 

    def testList(self):
        print("Preparando inicio Test Listado de Alumnos")
        self.assertEqual(self.listStudents, System.list(),"Fallo la lista de alumnos")

    def tearDown(self):
        MapperTest()
        
if __name__ == '__main__':
    unittest.main()