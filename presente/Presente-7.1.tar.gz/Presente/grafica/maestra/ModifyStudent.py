import time

from PyQt5                      import uic
from PyQt5.QtGui                import QIcon
from variablesGlobales          import CONFIG_UI,PATH_IMAGEN
from logica.Student             import Student
from logica.Usefull             import Usefull
from logica.System              import System
from logica.PDF                 import PDF
from grafica.Language           import Language

class ModifyStudent:
    def __init__(self,graphics,language):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow       = uic.loadUi(CONFIG_UI+"modificar.ui")
        self.graphics         = graphics
        
        self.__identification = 0
        
        self.idiom(language)
        
        #Eventos
        self.MainWindow.btnMenu.clicked.connect(self.back)        
        self.MainWindow.btnGuardar.clicked.connect(self.save)
        self.MainWindow.closeEvent = self.closeEvent
        
        
        self.MainWindow.setWindowIcon(QIcon(PATH_IMAGEN+'icono.ico'))
        
    
    def idiom(self,language):
        self.__language       = language
        #Etiquetas
        self.MainWindow.lblNombre.setText(self.__language.MESSAGE_FIRSTNAME)
        self.MainWindow.lblApellido.setText(self.__language.MESSAGE_LASTNAME)
        self.MainWindow.lblCedula.setText(self.__language.MESSAGE_IDENTICATION)
        self.MainWindow.lblTelefono.setText(self.__language.MESSAGE_PHONE)
        self.MainWindow.lblMaterno.setText(self.__language.MESSAGE_MOTHER_MAIL)
        self.MainWindow.lblPaterno.setText(self.__language.MESSAGE_FATHER_MAIL)
        self.MainWindow.lblAlumnos.setText(self.__language.MESSAGE_STUDENT)
        self.MainWindow.letCedula.setEnabled(False)
        
        #Botones
        self.MainWindow.btnGuardar.setText(self.__language.BUTTON_SAVE)
        self.MainWindow.btnMenu.setText(self.__language.BUTTON_BACK)
        
        #titulo
        self.MainWindow.setWindowTitle(self.__language.TITLE_MODIFY)
    def closeEvent(self, event):
        event.ignore()
        self.back()
    
            
    def toUpdate(self):
        student=System.find(self.__identification)
        self.MainWindow.letNombre.setText(student.getFirstName())
        self.MainWindow.letApellido.setText(student.getLastName())
        self.MainWindow.letCedula.setText(student.getIdentification())
        self.MainWindow.letTelefono.setText(student.getPhone())
        self.MainWindow.letMaterno.setText(student.getMotherMail())
        self.MainWindow.letPaterno.setText(student.getFatherMail())


    def save(self):
        self.MainWindow.lblMensaje.setText(Language.getInstance().MESSAGE_PROCESS)
        time.sleep(1)
        lastName         = self.MainWindow.letApellido.text().strip()
        firstName        = self.MainWindow.letNombre.text().strip()
        identification   = Usefull.identification(self.MainWindow.letCedula.text().strip())
        phone            = self.MainWindow.letTelefono.text().strip()
        fatherMail       = self.MainWindow.letPaterno.text().strip()
        motherMail       = self.MainWindow.letMaterno.text().strip()
        
        if len(firstName)==0:
            self.MainWindow.lblMensaje.setText(Language.getInstance().ERROR_FIELD_EMPTY_FIRSTNAME)
        else:
            if not Usefull.isName(self.__language,firstName):
                self.MainWindow.lblMensaje.setText(Language.getInstance().ERROR_FIELD_INVALID_FIRSTNAME)
            else:
                if len(lastName)==0:
                    self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_EMPTY_LASTNAME)
                else:
                    if not Usefull.isName(self.__language,lastName):
                        self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_INVALID_LASTNAME)
                    else:
                        if len(phone)==0:
                            self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_EMPTY_PHONE)
                        else:
                            if  len(fatherMail)>0 and not Usefull.es_correo_valido(fatherMail):
                                self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_INVALID_MAIL_FATHER)
                            else:
                                if  len(motherMail)>0 and not Usefull.es_correo_valido(motherMail):
                                    self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_INVALID_MAIL_MOTHER)
                                else:
                                    if not Usefull.isPhone(self.__language,phone):
                                        self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_INVALID_PHONE)
                                    else:
                                        if len(motherMail)>0 and motherMail==fatherMail:
                                            self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_MAIL_IDENTICAL)
                                        else:
                                            student = Student(firstName,lastName,identification ,phone,fatherMail,motherMail)
                                            System.save(student)
                                            PDF.generar(student)
                                            self.MainWindow.lblMensaje.setText( self.__language.MESSAGE_MODIFY )

    def back(self):
        self.graphics.windows("Students")
        
    def show(self):
        self.MainWindow.show()
        
    def hide(self):
        self.MainWindow.hide()

    def setIdentification(self,identification):
        self.__identification=identification
