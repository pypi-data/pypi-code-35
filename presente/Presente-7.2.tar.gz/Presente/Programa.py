import sys
import time

from PyQt5                       import QtWidgets,uic
from variablesGlobales           import CONFIG_UI
from grafica.Graphics            import Graphics
from grafica.Language            import Language
from grafica                     import imagenes_rc

class Programa:

    def __init__(self):
        # Cargamos la GUI desde el archivo UI.
        self.MainWindow = uic.loadUi(CONFIG_UI+"splash.ui")

    def mensaje(self,valor):
        if valor<30:
            self.MainWindow.lblEstado.setText(self.__language.SPLASH_WELCOME)
        else:
            if valor>=30 and valor<=60:
                self.MainWindow.lblEstado.setText(self.__language.SPLASH_NOTEBOOK)
            else:
                self.MainWindow.lblEstado.setText( self.__language.SPLASH_GREETING)    

    def iniciar(self,app):
        self.__language=Language()
        for i in range(10, 101,10):
            self.MainWindow.pgrBarra.setValue(i)
            self.mensaje(i)
            time.sleep(1)
            app.processEvents()

        graphics=Graphics(self,self.__language);
        graphics.windows("menu")

app         = QtWidgets.QApplication(sys.argv)
programa    = Programa()
programa.MainWindow.show()
programa.iniciar(app)
app.exec_()