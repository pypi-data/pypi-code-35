from PyQt5                      import uic
from PyQt5.QtGui                import QIcon
from variablesGlobales          import CONFIG_UI,PATH_IMAGEN,CONFIG_PATH
from logica.System              import System
from configparser               import ConfigParser
from datetime                   import datetime

class QueryStudent:
    def __init__(self,graphics, language):
        self.__graphics = graphics
        self.MainWindow = uic.loadUi(CONFIG_UI+"consultas.ui")
        self.idiom(language)
        config          = ConfigParser()
        config.read(CONFIG_PATH)
        start          = config.get("datos", "inicioClase")
        final          = config.get("datos", "finClase")
    
         # Cargamos la GUI desde el archivo UI.
        
        self.MainWindow.detDesde.setDateTime(datetime.strptime(start, '%d/%m/%y'))
        self.MainWindow.detHasta.setDateTime(datetime.strptime(final, '%d/%m/%y'))
                
        #Eventos
        self.MainWindow.closeEvent = self.closeEvent
        self.MainWindow.btnMenu.clicked.connect(self.back)
        self.MainWindow.btnLista.clicked.connect(self.listClass)
        
        
        self.MainWindow.setWindowIcon(QIcon(PATH_IMAGEN+'icono.ico'))
        
        self.MainWindow.ckxClase.stateChanged.connect(self.active)
        lis=[]
        self.__listStudents = System.list()
        for student in self.__listStudents:
            lis.append(student.fullName())
        self.MainWindow.cmoAlumnos.clear()
        self.MainWindow.cmoAlumnos.addItems(lis)
    
    def idiom(self,language):
        self.__language = language
        self.MainWindow.ckxClase.setText(self.__language.MESSAGE_CLASS_ALL)
        self.MainWindow.gbxInasistencias.setTitle(self.__language.MESSAGE_NO_ATTENDANCE)
        self.MainWindow.lblAlumnos.setText(self.__language.MESSAGE_STUDENT)
        self.MainWindow.lblDesde.setText(self.__language.MESSAGE_SINCE)
        self.MainWindow.lblHasta.setText(self.__language.MESSAGE_UNTIL)
        self.MainWindow.lblConsultas.setText(self.__language.MESSAGE_QUERY)
        
        #Botones
        self.MainWindow.btnConsultar.setText(self.__language.BUTTON_QUERY)
        self.MainWindow.btnLista.setText(self.__language.BUTTON_STUDENT_LIST)
        self.MainWindow.btnMenu.setText(self.__language.BUTTON_MENU)
        
        #Titulo
        self.MainWindow.setWindowTitle(self.__language.TITLE_QUERY_STUDENT)
    def active(self):
        self.MainWindow.cmoAlumnos.setEnabled(not self.MainWindow.ckxClase.isChecked())
    
    def closeEvent(self, event):
        event.ignore()
        self.back()

    def listClass(self):
        self.__graphics.windows("Students")
        
    def back(self):
        self.__graphics.back()
        
    def show(self):
        self.MainWindow.show()

    def hide(self):
        self.MainWindow.hide()
    
    def toUpdate(self):
        pass