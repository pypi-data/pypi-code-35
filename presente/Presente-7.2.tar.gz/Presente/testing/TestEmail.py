import unittest
from logica.Email   import Email
from logica.Student import Student
class TestEmail(unittest.TestCase):

    def testSend(self):
        student1=Student('Carlos','Sanchez',123,'099','bravo.india.tango2019@gmail.com','carlosalesanchez@gmail.com')
        email=Email()
        email.add(student1)
        email.sendAll()

if __name__ == '__main__':
    unittest.main()