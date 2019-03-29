from PyQt5                      import uic,QtCore
from PyQt5.QtGui                import QIcon
from PyQt5.QtWidgets            import QMessageBox,QTableWidgetItem,QProgressBar
from variablesGlobales          import CONFIG_UI,PATH_IMAGEN
from logica.System              import System

class Students:
    def __init__(self,graphics,language):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"listaAlumnos.ui")
        self.__graphics = graphics
        
        self.__listStudents =[]
        
        self.idiom(language)
        self.MainWindow.btnFicha.clicked.connect(self.see)
        
        self.MainWindow.btnMenu.clicked.connect(self.back)
        
        self.MainWindow.closeEvent = self.closeEvent
        
        
        self.MainWindow.setWindowIcon(QIcon(PATH_IMAGEN+'icono.ico'))
        
    def idiom(self,language):
        self.__language = language
        
        
        
        #Label
        self.MainWindow.lblLista.setText(self.__language.MESSAGE_LIST_STUDENT)
        
        #Boton
        self.MainWindow.btnMenu.setText(self.__language.BUTTON_MENU)
        self.MainWindow.btnFicha.setText(self.__language.BUTTON_STUDENT_SEE)
        self.MainWindow.btnImprimir.setText(self.__language.BUTTON_LIST_PRINT)
        
        #tabla
        self.MainWindow.tbeAlumnos.setHorizontalHeaderLabels((self.__language.COLUMN_FIRSTNAME, self.__language.COLUMN_LASTNAME,self.__language.COLUMN_IDENTIFICATION,self.__language.COLUMN_SKIPPED,self.__language.COLUMN_PRESENT,self.__language.COLUMN_PORCENTAGE))  # set header text
        self.MainWindow.gbxAlumnos.setTitle(self.__language.MESSAGE_STUDENT)
        
        #Titulo
        self.MainWindow.setWindowTitle(self.__language.TITLE_STUDENT_LIST)
        
    def closeEvent(self, event):
        event.ignore()
        self.back()       
    def see(self):
        if self.MainWindow.tbeAlumnos.currentItem() is None:
            QMessageBox.about(self.MainWindow,self.__language.MESSAGE_SYSTEM, self.__language.ERROR_SELECTION_ROW)
        else:
            positionRow    = self.MainWindow.tbeAlumnos.currentItem().row()
            identification =self.MainWindow.tbeAlumnos.item(positionRow,2).text()
            self.__graphics.StudentTab(identification)
    def back(self):
        self.__graphics.back()
        
    def show(self):
        self.MainWindow.show()
        
    def hide(self):
        self.MainWindow.hide()
    
    def toUpdate(self):
        
        self.MainWindow.tbeAlumnos.clear()
        #tabla
        self.MainWindow.tbeAlumnos.setColumnCount(6)
        self.MainWindow.tbeAlumnos.setHorizontalHeaderLabels((self.__language.COLUMN_FIRSTNAME, self.__language.COLUMN_LASTNAME,self.__language.COLUMN_IDENTIFICATION,self.__language.COLUMN_SKIPPED,self.__language.COLUMN_PRESENT,self.__language.COLUMN_PORCENTAGE))  # set header text
       
        self.__listStudents = System.list()
        self.MainWindow.tbeAlumnos.setRowCount(len(self.__listStudents))
        row=0
        for student in self.__listStudents:
            data=[student.getFirstName(),student.getLastName(),student.getIdentification(),student.getSkipped(),student.getPresent(),student.getTotal()]

            for column in range(0,len(data)):
                cellinfo=QTableWidgetItem(str(data[column]))
                cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.MainWindow.tbeAlumnos.setItem(row, column, cellinfo)
                if(5==column):
                    pgrAssitence = QProgressBar()
                    if data[3]>0:
                        pgrAssitence.setValue(data[4]*100/data[3])
                    else:
                        pgrAssitence.setValue(100)
                    self.MainWindow.tbeAlumnos.setCellWidget(row,5, pgrAssitence)
            row=row+1
        