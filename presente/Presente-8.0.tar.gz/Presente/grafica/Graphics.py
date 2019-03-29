from grafica.maestra.CardStudent   import CardStudent
from grafica.maestra.PassList      import PassList
from grafica.maestra.Help          import Help
from grafica.maestra.Students      import Students
from grafica.maestra.StudentTab    import StudentTab
from grafica.Menu                  import Menu
from grafica.maestra.ModifyStudent import ModifyStudent
from grafica.maestra.QueryStudent  import QueryStudent
from grafica.Language              import Language 
import sys
import subprocess

class Graphics:

    def __init__(self,ventana,language):
        self.__ventana=ventana
        self.__list = {'HELP':Help(self,language),'MENU':Menu(self,language),'CARDSTUDENT': CardStudent(self,language), 'PASSLIST': PassList(self,language),'QUERYSTUDENT':QueryStudent(self,language),'STUDENTS':Students(self,language),'STUDENTS_TAB':StudentTab(self,language),'MODIFY_STUDENT':ModifyStudent(self,language)}

    def language(self,language):
        
        idiom=Language(language)
        
        for key in self.__list:
            window=self.__list[key]
            window.idiom(idiom)
        
        
    def ocultar(self):
        for key in self.__list:
            self.__list[key].hide()

    def vaciar(self):
        del self.__list['STUDENTS']

    def windows(self,window):
        self.ocultar()
        self.__ventana.MainWindow=self.__list[window.upper()]
        self.__ventana.MainWindow.toUpdate()
        self.__ventana.MainWindow.show()   
        
    def StudentTab(self,identification):
        self.__ventana.MainWindow=self.__list['STUDENTS_TAB']
        self.__ventana.MainWindow.setIdentification(identification)
        self.windows('STUDENTS_TAB')
    
    def ModifyStudent(self,identification):
        self.__ventana.MainWindow=self.__list['MODIFY_STUDENT']
        self.__ventana.MainWindow.setIdentification(identification)
        self.windows('MODIFY_STUDENT')
        
    def back(self):
        self.windows("Menu")

    def openFile(self, file):
        subprocess.Popen([file],shell=True)