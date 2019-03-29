import time
import os
from PyQt5                      import uic
from PyQt5.QtWidgets            import QMessageBox
from PyQt5.QtGui                import QIcon

from variablesGlobales          import CONFIG_UI,PATH_IMAGEN,CONFIG_PDF
from logica.Student             import Student
from logica.Usefull             import Usefull
from logica.System              import System
from logica.PDF                 import PDF
from grafica.Language           import Language

class CardStudent:
    def __init__(self,graphics,language):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"alumnos.ui")
        self.graphics   = graphics

        self.idiom(language)

        #Eventos
        self.MainWindow.btnMenu.clicked.connect(self.back)
        self.MainWindow.btnQr.clicked.connect(self.print)
        self.MainWindow.btnGuardar.clicked.connect(self.save)
        self.MainWindow.btnNuevo.clicked.connect(self.clear)
        self.MainWindow.btnBuscar.clicked.connect(self.find)
        self.MainWindow.btnEliminar.clicked.connect(self.delete)
        self.MainWindow.closeEvent = self.closeEvent
        
        
        self.MainWindow.setWindowIcon(QIcon(PATH_IMAGEN+'icono.ico'))
        
    def idiom(self,language):
        self.__language=language
        
        #Etiquetas
        self.MainWindow.lblNombre.setText(self.__language.MESSAGE_FIRSTNAME)
        self.MainWindow.lblApellido.setText(self.__language.MESSAGE_LASTNAME)
        self.MainWindow.lblCedula.setText(self.__language.MESSAGE_IDENTICATION)
        self.MainWindow.lblTelefono.setText(self.__language.MESSAGE_PHONE)
        self.MainWindow.lblMaterno.setText(self.__language.MESSAGE_MOTHER_MAIL)
        self.MainWindow.lblPaterno.setText(self.__language.MESSAGE_FATHER_MAIL)
        self.MainWindow.lblAlumnos.setText(self.__language.MESSAGE_STUDENT)

        #Botones
        self.MainWindow.btnNuevo.setText(self.__language.BUTTON_NEW)
        self.MainWindow.btnGuardar.setText(self.__language.BUTTON_SAVE)
        self.MainWindow.btnEliminar.setText(self.__language.BUTTON_DELETE)
        self.MainWindow.btnQr.setText(self.__language.BUTTON_QR_PRINT)
        self.MainWindow.btnMenu.setText(self.__language.BUTTON_MENU)
        self.MainWindow.btnBuscar.setText(self.__language.BUTTON_FIND)
        self.clear()
        
        #Titulo
        self.MainWindow.setWindowTitle(self.__language.TITLE_CARD_STUDENT)
        
    def print(self):
        identification = self.MainWindow.letCedula.text()
        student        = System.find(identification)
        path           = CONFIG_PDF+"\\"+str(student)+".pdf"

        if not os.path.isfile(path):
            System.generarQR(identification)

        self.graphics.openFile(path)
    def closeEvent(self, event):
        event.ignore()
        self.back()
    
    def delete(self):
        buttonReply = QMessageBox.question(self.MainWindow, 'Sistema...', "Desea eliminar el alumno?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if buttonReply == QMessageBox.Yes:
            System.delete(Usefull.identification(self.MainWindow.letCedula.text().strip()))
            self.MainWindow.lblMensaje.setText(self.__language.MESSAGE_DELETE_STUDENT)
            self.clear()
        
    def find(self):
        identification = Usefull.identification(self.MainWindow.letCedula.text().strip())
        self.clear()
        if len(identification)==0:
            self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIND_IDENTIFICATION)
        else:
            student=System.find(identification)
            if student is None:
                self.MainWindow.lblMensaje.setText(self.__language.ERROR_NOT_FIND)
            else:
                self.MainWindow.btnQr.setEnabled(True)
                self.MainWindow.btnEliminar.setEnabled(True)
                self.MainWindow.letNombre.setText(student.getFirstName())
                self.MainWindow.letApellido.setText(student.getLastName())
                self.MainWindow.letCedula.setText(student.getIdentification())
                self.MainWindow.letTelefono.setText(student.getPhone())
                self.MainWindow.letMaterno.setText(student.getMotherMail())
                self.MainWindow.letPaterno.setText(student.getFatherMail())
                self.MainWindow.letCedula.setEnabled(False)
                self.MainWindow.btnNuevo.setEnabled(True)
            
    def toUpdate(self):
        pass
        
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
                                        if len(identification)==0:
                                            self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_EMPTY_IDENTIFICATION)
                                        else:
                                            if len(motherMail)>0 and motherMail==fatherMail:
                                                self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_MAIL_IDENTICAL)
                                            else:
                                                if not Usefull.isIdentificationUruguay(identification):
                                                    self.MainWindow.lblMensaje.setText(self.__language.ERROR_FIELD_IDENTIFICATION)
                                                else:
                                                    
                                                    student        = Student(firstName,lastName,identification ,phone,fatherMail,motherMail)
                                                    identification = Usefull.identification(self.MainWindow.letCedula.text().strip())
                                                    student2=System.find(identification)
                                                    if student2 is None or not self.MainWindow.letCedula.isReadOnly():
                                                        System.save(student)
                                                        if student2 is None:
                                                            PDF.generar(student)
                                                            self.MainWindow.lblMensaje.setText( self.__language.MESSAGE_OK_SAVE_STUDENT )
                                                            path           = CONFIG_PDF+"\\"+str(student)+".pdf"
                                                            self.graphics.openFile(path)
                                                        else:
                                                            self.MainWindow.lblMensaje.setText( self.__language.MESSAGE_MODIFY )
                                                        self.clear()
                                                    else:   
                                                        self.MainWindow.lblMensaje.setText(self.__language.ERROR_THERE_IS_REGISTERED)

    def clear(self):
        self.MainWindow.letApellido.setText("")
        self.MainWindow.letNombre.setText("")
        self.MainWindow.letCedula.setText("")
        self.MainWindow.letTelefono.setText("")
        self.MainWindow.letMaterno.setText("")
        self.MainWindow.letPaterno.setText("")
        self.MainWindow.btnQr.setEnabled(False)
        self.MainWindow.btnQr.setEnabled(False)
        self.MainWindow.btnNuevo.setEnabled(False)
        self.MainWindow.letCedula.setEnabled(True)
        self.MainWindow.btnEliminar.setEnabled(False)
        
    def back(self):
        self.clear()
        self.MainWindow.lblMensaje.setText("")
        self.graphics.back()
        
    def show(self):
        self.MainWindow.show()
        
    def hide(self):
        self.MainWindow.hide()
