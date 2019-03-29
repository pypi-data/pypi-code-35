
import qrcode
import pyzbar.pyzbar as pyzbar
from   logica.Student     import Student
from   variablesGlobales  import CONFIG_IMG

class QR:

    @staticmethod
    def generate(student):
        image  = qrcode.make(student.getIdentification())
        file = open(CONFIG_IMG, "wb")
        image.save(file)
        file.close()

    @staticmethod
    def decode(image):
        # Find barcodes and QR codes
        decodedObjects = pyzbar.decode(image)
        # Print results
#        for obj in decodedObjects:
#            print('Type : ', obj.type)
#            print('Data : ', obj.data,'\n')     
        return decodedObjects
