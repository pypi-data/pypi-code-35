from PyQt5                      import uic
from PyQt5.QtGui                import QIcon
from PyQt5.QtWidgets            import QMessageBox
from variablesGlobales          import CONFIG_UI,PATH_IMAGEN,CONFIG_PDF
from logica.System              import System
from logica.PDFStudent          import PDFStudent
import os.path

class StudentTab:
    def __init__(self,graphics,language):
        
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"fichaAlumno.ui")
        self.__graphics = graphics
        
        self.__identification=0
        
        self.idiom(language)
        self.MainWindow.closeEvent = self.closeEvent
        
        #Boton
        self.MainWindow.btnMenu.clicked.connect(self.back)        
        self.MainWindow.btnQr.clicked.connect(self.print)
        self.MainWindow.btnEliminar.clicked.connect(self.delete)
        self.MainWindow.btnGuardar.clicked.connect(self.modify)
        self.MainWindow.btnImprimir.clicked.connect(self.studentPrint)
        self.MainWindow.setWindowIcon(QIcon(PATH_IMAGEN+'icono.ico'))
    
    def studentPrint(self):
        identification = self.MainWindow.lblCedulaData.text()
        student        = System.find(identification)
        pdf=PDFStudent()
        pdf.generar(student)
        path=CONFIG_PDF+"\\Ficha\\Ficha_"+str(student)+".pdf"
        self.__graphics.openFile(path)
        
    def idiom(self,language):
        self.__language = language
        #Etiquetas
        self.MainWindow.lblAlumnos.setText(self.__language.MESSAGE_STUDENT_TAB)
        self.MainWindow.lblNombre.setText(self.__language.MESSAGE_FIRSTNAME)
        self.MainWindow.lblApellido.setText(self.__language.MESSAGE_LASTNAME)
        self.MainWindow.lblCedula.setText(self.__language.MESSAGE_IDENTICATION)
        self.MainWindow.lblTelefono.setText(self.__language.MESSAGE_PHONE)
        self.MainWindow.lblMaterno.setText(self.__language.MESSAGE_MOTHER_MAIL)
        self.MainWindow.lblPaterno.setText(self.__language.MESSAGE_FATHER_MAIL)
        self.MainWindow.lblInasistencias.setText(self.__language.MESSAGE_ABSENCE)
        self.MainWindow.setWindowTitle(self.__language.TITLE_STUDENT_TAB)
        
        #Boton

        self.MainWindow.btnGuardar.setText(self.__language.BUTTON_SAVE)
        self.MainWindow.btnEliminar.setText(self.__language.BUTTON_DELETE)
        self.MainWindow.btnQr.setText(self.__language.BUTTON_QR_PRINT)
        self.MainWindow.btnMenu.setText(self.__language.BUTTON_MENU)
        self.MainWindow.btnImprimir.setText(self.__language.BUTTON_STUDENT_PRINT)
        
    def modify(self):
        self.__graphics.ModifyStudent(self.MainWindow.lblCedulaData.text())
        
    def delete(self):
        buttonReply = QMessageBox.question(self.MainWindow, 'Sistema...', "Desea eliminar el alumno?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if buttonReply == QMessageBox.Yes:
           System.delete(self.MainWindow.lblCedulaData.text().strip())
           QMessageBox.about(self.MainWindow,self.__language.MESSAGE_SYSTEM, self.__language.MESSAGE_DELETE_STUDENT)
           self.back()
                
    def print(self):
        identification = self.MainWindow.lblCedulaData.text()
        student        = System.find(identification)
        path           = CONFIG_PDF+"\\"+str(student)+".pdf"
        if not os.path.isfile(path):
            System.generarQR(identification)
        
        self.__graphics.openFile(path)
        
    def closeEvent(self, event):
        event.ignore()
        self.back()
        
    def setIdentification(self,identification):
        self.__identification=identification
        
    def back(self):
        self.__graphics.windows("STUDENTS")
        
    def show(self):
        self.MainWindow.show()
        
    def hide(self):
        self.MainWindow.hide()
        
    def mail(self,mail):
        if mail=="":
            return self.__language.MESSAGE_NOT_REGISTERED
        else:
            return mail
        
    def toUpdate(self):
        student=System.find(self.__identification)
        self.MainWindow.lblNombreData.setText(student.getFirstName())
        self.MainWindow.lblApellidoData.setText(student.getLastName())
        self.MainWindow.lblCedulaData.setText(student.getIdentification())
        self.MainWindow.lblTelefonoData.setText(student.getPhone())
        self.MainWindow.lblMaternoData.setText(self.mail(student.getMotherMail()))
        self.MainWindow.lblPaternoData.setText(self.mail(student.getFatherMail()))
        self.MainWindow.lblInasistenciasData.setText(str(student.getSkipped()))
        