import sys
 
from PyQt5                         import uic
from PyQt5.QtGui                   import QIcon
from PyQt5.QtWidgets               import QSystemTrayIcon, QMenu,QMessageBox,QAction
from variablesGlobales             import CONFIG_UI,PATH_IMAGEN
from logica.System                 import System
from logica.Email                  import Email
from logica.Usefull                import Usefull


class Menu:
    def __init__(self,graphics,language):
        
        self.graphics=graphics
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"menu.ui")

        self.MainWindow.systray = QSystemTrayIcon(QIcon(PATH_IMAGEN+"icono.ico"), self.MainWindow)
        self.MainWindow.systray.show()

        # Crear el menú contextual.
        self.systray_menu = QMenu(self.MainWindow)
        
        #idioma
        sub_menu = self.systray_menu.addMenu("Idioma")
        
        #Español
        subEspaniol = QAction("&Español",sub_menu)
        subEspaniol.setShortcut("Ctrl+E")
        subEspaniol.setStatusTip('Poner en español')
        subEspaniol.triggered.connect(self.idiomSpanish)
        subEspaniol.setChecked(True)
        sub_menu.addAction(subEspaniol)
        
        #ingles
        subIngles = QAction("&Ingles",sub_menu)
        subIngles.setShortcut("Ctrl+I")
        subIngles.setStatusTip('Poner en Ingles')
        subIngles.triggered.connect(self.idiomIngles)
        sub_menu.addAction(subIngles)
        
        #Portuges
        subPortugues = QAction("&Portugues",sub_menu)
        subPortugues.setShortcut("Ctrl+P")
        subPortugues.setStatusTip('Poner en Portugues')
        subPortugues.triggered.connect(self.idiomPortugues)
        sub_menu.addAction(subPortugues)
    
        self.MainWindow.systray.setContextMenu(self.systray_menu)
        
        self.MainWindow.setWindowIcon(QIcon(PATH_IMAGEN+'icono.ico'))

        self.idiom(language)
        
        #Eventos
        self.MainWindow.btnSalir.clicked.connect(self.exit)
        self.MainWindow.btnLista.clicked.connect(self.list)
        self.MainWindow.btnAlumnos.clicked.connect(self.card)
        self.MainWindow.btnConsulta.clicked.connect(self.query)  
        self.MainWindow.btnAyuda.clicked.connect(self.help)
        self.MainWindow.closeEvent = self.closeEvent
        
        self.salir=False
        print(Usefull.today())
        
        
    def idiom(self,language):
        self.language=language
        #Label
        self.MainWindow.lblMenu.setText(self.language.MESSAGE_MENU)
        
        #Boton
        self.MainWindow.btnSalir.setText(self.language.BUTTON_EXIT)
        self.MainWindow.btnLista.setText(self.language.BUTTON_PASS_LIST)
        self.MainWindow.btnAlumnos.setText(self.language.BUTTON_STUDENTS)
        self.MainWindow.btnConsulta.setText(self.language.BUTTON_QUERY)
        self.MainWindow.btnAyuda.setText(self.language.BUTTON_HELP)
        
        #title
        self.MainWindow.setWindowTitle(self.language.TITLE_MAIN)
        
    def closeEvent(self, event):
       
            event.ignore()
            self.exit()

    def idiomSpanish(self):
        
        self.graphics.language("es")
    
    def idiomPortugues(self):
        self.graphics.language("pt")
    def idiomIngles(self):
        self.graphics.language("en")
        

    def help(self):
        self.graphics.windows("Help")
        
    def query(self):
        self.graphics.windows("QueryStudent")
    
    def changeScreen(self,window):
        self.graphics.windows(window)
        
    def hide(self):
        self.MainWindow.hide()
   
    def show(self):
        self.MainWindow.show()
        
    def exit(self):
        buttonReply = QMessageBox.question(self.MainWindow, self.language.MESSAGE_SYSTEM, self.language.MESSAGE_EXIT, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if buttonReply == QMessageBox.Yes:
            if System.isWanting():
                buttonReply = QMessageBox.question(self.MainWindow, self.language.MESSAGE_SYSTEM, self.language.MESSAGE_SEND_MAIL, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    email=Email(self.language.TEMPLATE_MAIL)
                    System.closing(Usefull.today(),Usefull.today())
                    fechaGenerado=System.wanting(Usefull.today())
                    for student in fechaGenerado.getStudentsList():
                        email.add(student)
                    email.sendAll()
            self.graphics.vaciar()
            sys.exit()

    def list(self):
        self.graphics.windows("PassList")

    def toUpdate(self):
        if not System.isWanting():
            self.MainWindow.btnLista.setEnabled(False)
            self.MainWindow.btnLista.setToolTip(self.language.MESSAGE_CAME_ALL) 
        else:
            self.MainWindow.btnLista.setEnabled(True)
            self.MainWindow.btnLista.setToolTip('')
    def card(self):
        self.graphics.windows("CardStudent")
