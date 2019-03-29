from PyQt5                      import uic
from PyQt5.QtCore               import Qt
from PyQt5.QtGui                import QIcon
from variablesGlobales          import CONFIG_UI,PATH_IMAGEN
from PyQt5.QtWidgets            import QStackedWidget,QTreeWidgetItem,QLabel
import webbrowser


TreeList = ({

    'Funcionamiento': ((
        'Agregar Alumno',
        'Busqueda y modificar Alumno',
        'Eliminar Alumno',
        'Volver imprimir QR de un alumno',
        'Pasar la lista con QR',
        'Pasar la lista manual',
        'Como cerrar la libreta'
        
    )),

    'Consejos': ((
        'Blog'
    ))
})

paginas=['https://www.iorad.com/player/1557425/Ingresar-un-alumno-al-sistema',
         'https://www.iorad.com/player/1557512/Busqueda-y-modificacion-del-alumno',
         'https://www.iorad.com/player/1557524/Como-eliminar-un-alumno',
         'https://www.iorad.com/player/1557538/Volver-imprimir-las-QR',
         'https://www.iorad.com/player/1557565/Pasar-la-lista-por-la-QR',
         'https://www.iorad.com/player/1557570/Pasar-la-lista-de-forma-manual',
         'https://www.iorad.com/player/1557577/Como-cerrar-la-libreta-del-dia',
         'https://presentebit.blogspot.com'
        ]

class Help:
    def __init__(self,graphics,language):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"Help.ui")
        self.graphics = graphics
        self.MainWindow.stack = QStackedWidget(self.MainWindow)
        self.MainWindow.setWindowIcon(QIcon(PATH_IMAGEN+'icono.ico'))
        
        
        for key, value in TreeList.items():
            root = QTreeWidgetItem(self.MainWindow.twtPreguntas, [key])
            for val in value:
                item = QTreeWidgetItem([val])
                root.addChild(item)
                
                widget = QLabel(val,  self.MainWindow)
                ix = self.MainWindow.stack.addWidget(widget)
                item.setData(0, Qt.UserRole, ix)
        
        self.MainWindow.twtPreguntas.expandAll()
        self.MainWindow.twtPreguntas.itemClicked.connect(self.onItemClicked)

        self.idiom(language)
        
        #Boton

        self.MainWindow.btnMenu.clicked.connect(self.back)
        self.MainWindow.closeEvent = self.closeEvent
        
    def onItemClicked(self, item, column):
        val = item.data(0, Qt.UserRole)
        if val is not None:
            webbrowser.open(paginas[val], new=2, autoraise=True)
            
    def idiom(self,language):
        self.language=language
        
        #Label
        self.MainWindow.lblAyuda.setText(self.language.MESSAGE_HELP)
        self.MainWindow.gbxPreguntas.setTitle(self.language.MESSAGE_FREQUENTLY_ASKED)
        self.MainWindow.btnMenu.setText(self.language.BUTTON_MENU)
        
        #titulo
        self.MainWindow.setWindowTitle(self.language.TITLE_HELP)
    def closeEvent(self, event):
        event.ignore()
        self.back()
        
#    def play(self):
       
# 
    def back(self):
        self.graphics.back()
        
    def show(self):
        self.MainWindow.show()
        
    def hide(self):
        self.MainWindow.hide()
    
    def toUpdate(self):
        pass