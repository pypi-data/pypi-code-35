import unittest

from grafica.Language         import Language
from logica.Usefull           import Usefull

class TestUsefull(unittest.TestCase):

    def setUp(self):
        print("Preparando informacion Test Usefull")
        self.language=Language()

    def testAncel(self):
        print("Test Celulares Ancel")
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"099276901"))
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"098276901"))
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"091276901"))
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"092276901"))
    
    def testMovistar(self):
        print("Test Celulares Movistar")
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"093276901"))
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"094276901"))
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"095276901"))

    def testClaro(self):
        print("Test Celulares Claro")
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"096276901"))
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"097276901"))

    def testAntel(self):
        print("Test Celulares Antel")
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"29081764"))
        self.assertTrue(Usefull.isPhone(self.language.EXPRESSION_PHONE,"49081764"))

    def testNovalido(self):
        print("Test telefonos no valido")
        self.assertFalse(Usefull.isPhone(self.language.EXPRESSION_PHONE,"99276901"))
        self.assertFalse(Usefull.isPhone(self.language.EXPRESSION_PHONE,"090276901"))
        self.assertFalse(Usefull.isPhone(self.language.EXPRESSION_PHONE,"09127690"))
        self.assertFalse(Usefull.isPhone(self.language.EXPRESSION_PHONE,"092276901777"))
     
    def testIdentification(self):
        print("Test identificacion uruguaya")
        self.assertTrue(Usefull.isIdentificationUruguay(31075329))
         
