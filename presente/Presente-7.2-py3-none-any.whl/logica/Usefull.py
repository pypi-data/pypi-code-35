import re
import time
import sys
class Usefull:
    
    @staticmethod
    def identification(id):
        id=id.replace('.', '')
        id=id.replace('-', '')
        return id
    
     
    @staticmethod
    def es_correo_valido(correo):
        correo=correo.lower()
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(expresion_regular, correo) is not None
    
    @staticmethod
    def isPhone(language,phone):
        return re.match(language.EXPRESSION_PHONE, phone) is not None
    
    @staticmethod
    def isName(language,name):
        return re.match(language.EXPRESSION_NAME, name) is not None    
    
    @staticmethod
    def today():
        return time.strftime("%d/%m/%y")     
    
    def unidad(x):
        return(x-(x//10)*10)

    def isNumeric(number):
        try:
            int(number)
            return True
        except ValueError:
            return False
            
    def isIdentificationUruguay(identification):
        identification = Usefull.identification(identification)
        lenID          = len(identification);
        print (Usefull.isNumeric(identification))
        if (lenID!=8 and lenID!=7) or not Usefull.isNumeric(identification):
            return False
                
        print('paso')
        id             = str(identification);
        numerSecret    = '2987634'  
        checker        = identification[-1]
        rest           = identification[:lenID - 1]
        suma=0  # un entero cero
        
        if len(rest)==6:
            rest = '0'+rest;  # se pone un cero en los millones
        
        for i in range(0,7):
            suma=suma+Usefull.unidad(int(id[i])*int(numerSecret[i]));
                    
        result      = 10-Usefull.unidad(suma);
        if result == 10:
            result  = 0;
        print('Resultado : '+str(result))
        print('ultimo digito : '+str(checker))
        return(int(result)==int(checker))
        
    