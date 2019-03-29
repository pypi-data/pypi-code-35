import unittest
import filecmp
from logica.Student           import Student
from logica.QR                import QR
from variablesGlobales        import CONFIG_IMG
from variablesGlobales        import TEST_IMG

class TestQR(unittest.TestCase):

    def setUp(self):
        print("Preparando inicio Test Lista")

        student1=Student('Carlos','Sanchez',123,'099','carlosalesanchez@gmail.com','carlosalesanchez@gmail.com')
        student2=Student('Franco','sssssss',321,'094','franco@gmail.com'          ,'franco@gmail.com')
        student3=Student('Sofia' ,'ddddddd',222,'093','sofia@gmail.com'           ,'sofia@gmail.com')
        student4=Student('Mai'   ,'fffffff',223,'097','mai@gmail.com'             ,'mai@gmail.com')

        self.listStudents=[student1,student2,student3,student4]
        
    def testQRSonIguales(self):
        print("Preparando inicio Test QR son iguales")
        QR.generate(self.listStudents[0])
        self.assertTrue(filecmp.cmp(TEST_IMG, CONFIG_IMG),"Fallo los archivos QR no son iguales")

    def testQRNoSonIguales(self):
        print("Preparando inicio Test QR son iguales")
        QR.generate(self.listStudents[1])
        self.assertFalse(filecmp.cmp(TEST_IMG, CONFIG_IMG),"Fallo los archivos QR son iguales")

if __name__ == '__main__':
    unittest.main()