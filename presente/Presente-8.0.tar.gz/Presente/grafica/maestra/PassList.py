from PyQt5                   import QtCore, QtGui,  uic
from PyQt5.QtGui             import QIcon
from variablesGlobales       import CONFIG_UI,PATH_IMAGEN
from logica.QR               import QR
from logica.System           import System
from logica.Email            import Email
from logica.Usefull          import Usefull
from PyQt5.QtWidgets         import QMessageBox
from logica.Audio            import Audio

import numpy as np
import cv2


class PassList:
    def __init__(self,graphics,language):
        self.graphics = graphics
        
        self.MainWindow = uic.loadUi(CONFIG_UI+"pasarLista.ui")
        self.idiom(language)
       
        
        #evento
        self.MainWindow.btnGuardar.clicked.connect(self.terminate)
        self.MainWindow.btnAgregar.clicked.connect(self.writeDownManual)
        self.MainWindow.btnMenu.clicked.connect(self.back)        
        self.MainWindow.closeEvent = self.closeEvent
        self.idiom(language)
        
        self.MainWindow.setWindowIcon(QIcon(PATH_IMAGEN+'icono.ico'))


        # Tomamos el dispositivo de captura a partir de la webcam.
        self.webcam = cv2.VideoCapture(0)
 
        # Creamos un temporizador para que cuando se cumpla el tiempo limite tome una captura desde la webcam.
        self.timer = QtCore.QTimer(self.MainWindow);
 
        # Conectamos la señal timeout() que emite nuestro temporizador con la funcion show_frame().
        self.timer.timeout.connect(self.show_frame)
 
        
        # Tomamos una captura cada 1 mili-segundo.
        self.timer.start(1);
        self.audio          = Audio()

        self.toUpdate()

        System.opening(Usefull.today())
        self.student        = None
        self.fechaGenerado  = System.wanting(Usefull.today())
        self.seguir         = True
        self.mensaje        = ""
    
    def idiom(self,language):
        self.language = language
         #Etiqueta
        self.MainWindow.lblLista.setText(self.language.MESSAGE_PASS_LIST)
        
        #Botones
        self.MainWindow.btnAgregar.setText(self.language.BUTTON_ADD_MANUAL)
        self.MainWindow.btnGuardar.setText(self.language.BUTTON_SAVE)
        self.MainWindow.btnMenu.setText(self.language.BUTTON_MENU)
        self.MainWindow.btnAgregar.setText(self.language.BUTTON_ADD_MANUAL)
        
        #titulo
        self.MainWindow.setWindowTitle(self.language.TITLE_PASS_LIST)
        
    def closeEvent(self, event):
        event.ignore()
        self.back()
        
    def toUpdate(self):
        lis=[]
        self.__listStudents = System.wanting(Usefull.today()).getStudentsList()
        for student in self.__listStudents:
            lis.append(student.fullName())
        self.MainWindow.cmoAlumnos.clear()
        self.MainWindow.cmoAlumnos.addItems(lis)
        
        lisStudentPresent=[]
        listPresent=System.lisPresentToday()
        for student in listPresent:
            lisStudentPresent.append(student.fullName())
        self.MainWindow.lstPresentes.clear()
        self.MainWindow.lstPresentes.addItems(lisStudentPresent)
        self.MainWindow.btnAgregar.setEnabled(True)
    
    def back(self):
        self.graphics.back()
    
    
    def writeDownManual(self):
        index = self.MainWindow.cmoAlumnos.currentIndex()
        student   = self.__listStudents[index];
        if not System.isPresent(student.getIdentification(),Usefull.today()):
            System.present(student.getIdentification(),Usefull.today())
            self.fechaGenerado  = System.wanting(Usefull.today())
            self.audio.play(student.fullName())
            self.MainWindow.lstPresentes.addItem(student.fullName())
            if self.fechaGenerado.empty():
                self.MainWindow.btnGuardar.setEnabled(False)
                System.closing(Usefull.today(),Usefull.today())
                QMessageBox.about(self.MainWindow,self.language.MESSAGE_SYSTEM, self.language.MESSAGE_PRESENT_ALL)
        else:
            self.audio.play("yaEstaba")
        
    def hide(self):
        self.MainWindow.hide()
        
    def terminate(self):
        System.closing(Usefull.today(),Usefull.today())
        fechaGenerado=System.wanting(Usefull.today())
        
        if len(fechaGenerado.getStudentsList())>0:
            email=Email(self.language.TEMPLATE_MAIL)
            for student in fechaGenerado.getStudentsList():
                email.add(student)
            email.sendAll()
            QMessageBox.about(self.MainWindow,self.language.MESSAGE_SYSTEM, self.language.MESSAGE_SEND_ALL)
        else:
            QMessageBox.about(self.MainWindow,self.language.MESSAGE_SYSTEM, self.language.MESSAGE_PRESENT_ALL)
        self.MainWindow.btnGuardar.setEnabled(False)
        
    def accredit(self,student):
        if not System.isPresent(student.getIdentification(),Usefull.today()):
            System.present(student.getIdentification(),Usefull.today())
            self.fechaGenerado  = System.wanting(Usefull.today())
            self.audio.play(student.fullName())
            self.MainWindow.lstPresentes.addItem(student.fullName())
            if self.fechaGenerado.empty():
                self.MainWindow.btnGuardar.setEnabled(False)
                System.closing(Usefull.today(),Usefull.today())
                QMessageBox.about(self.MainWindow,self.language.MESSAGE_SYSTEM, self.language.MESSAGE_PRESENT_ALL)
        else:
            self.audio.play("yaEstaba")
        
    def procesarImagen(self,imagen):
        image = QtGui.QImage(imagen, imagen.shape[1], imagen.shape[0], imagen.shape[1] * imagen.shape[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        
        # Mostramos el QPixmap en la QLabel.
        self.MainWindow.lblWebcam.setPixmap(pixmap)

    def detectQR(self,imagen):
        qr = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
         
        decodedObjects = QR.decode(qr)
        
        for decodedObject in decodedObjects: 
            points = decodedObject.polygon
         
            # If the points do not form a quad, find convex hull
            if len(points) > 4 : 
              hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
              hull = list(map(tuple, np.squeeze(hull)))
            else : 
              hull = points;
             
            # Number of points in the convex hull
            n = len(hull)     
            # Draw the convext hull
            for j in range(0,n):
              cv2.line(imagen, hull[j], hull[ (j+1) % n], (255,0,0), 3)
            
            return decodedObject,decodedObject.data.decode('ascii')
        return imagen,None
    
    def texto(self,imagen,decodedObject,mensaje):
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(imagen, mensaje, (decodedObject.rect.left, decodedObject.rect.top), font, 1, (0,255,255), 2, cv2.LINE_AA)
    """
    show_frame() -> None
 
    Esta funcion toma una captura desde la webcam y la muestra en una QLabel.
    """

    def show(self):
        self.MainWindow.show()

    def show_frame(self):
        # Tomamos una captura desde la webcam.
        ok, imagen = self.webcam.read()
        if not ok:
            return

        decodedObject,id=self.detectQR(imagen)
        if decodedObject is not None:
                if id is None:
                    pass
                else:
                    student=System.find(id)
                    if(student is None):
                        pass
                    else:
                        if not System.isPresent(student.getIdentification(),Usefull.today()):
                            self.__student =student
                            self.accredit(student) 
                        else:
                            if((self.student is None or student!=self.student)):
                                self.student =student
                                self.audio.play("yaEstaba")

        self.procesarImagen(imagen)
        
    def __del__(self):
        self.timer.stop()