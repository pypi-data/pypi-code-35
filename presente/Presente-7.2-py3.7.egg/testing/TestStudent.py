import unittest
from logica.Student           import Student
from logica.System            import System
from persistencia.MapperTest  import MapperTest
import doctest
doctest.testmod()

class TestStudent(unittest.TestCase):

    def setUp(self):
        print("Preparando inicio Test Student")
        MapperTest()
        student1=Student('Carlos','Sanchez',123,'099','carlosalesanchez@gmail.com','carlosalesanchez@gmail.com')
        student2=Student('Franco','sssssss',321,'094','franco@gmail.com'          ,'franco@gmail.com')
        student3=Student('Sofia' ,'ddddddd',222,'093','sofia@gmail.com'           ,'sofia@gmail.com')
        student4=Student('Mai'   ,'fffffff',223,'097','mai@gmail.com'             ,'mai@gmail.com')

        self.listStudents=[student1,student2,student3,student4]

    def testSave(self):
        print("Preparando inicio Test Agregar Student en la Base de Datos")
        for student in self.listStudents:
            System.save(student) 
        self.assertEqual(self.listStudents, System.list(),"No se agrego en la base de datos ")

    def testFind(self):
        print("Preparando inicio Test Buscar Student en la Base de Datos")
        for student in self.listStudents:
            System.save(student) 
        studentBase=System.find('123')
        self.assertEqual(studentBase, self.listStudents[0],"No se necontro el Student cuando deberia si lo contrario")

    def testNotFound(self):
        print("Preparando inicio Test No Encontrar Student en la Base de Datos")
        for student in self.listStudents:
            System.save(student) 
        studentBase=System.find('1235')
        self.assertIsNone(studentBase,"Test de no encontrar pero encontro")

    def tearDown(self):
        mapper=MapperTest()
        mapper.clear()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()