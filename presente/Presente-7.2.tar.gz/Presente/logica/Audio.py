from variablesGlobales import CONFIG_AUDIO,CONFIG_PATH,CONFIG_TEMP_AUDIO,CONFIG_AUDIO_SALUDOS
from gtts              import gTTS 
from configparser      import ConfigParser
import shutil
import pygame
import os 
import threading

class Audio:
    def __init__(self):
        
        config          = ConfigParser()
        config.read(CONFIG_PATH)
        self.__language = config.get("audio", "idioma")
        self.__speed    = config.get("audio", "velocidad")
        self.__play     = False
        
        
    def createGreeting(self,name): 
         self.createName(name)
         self.join(name)

    def createName(self,name):
         myobj    = gTTS(text=name, lang=self.__language, slow=self.__speed) 
         myobj.save(CONFIG_TEMP_AUDIO+"\\temp.mp3")
    
    def join(self,name):
        if not os.path.isfile(CONFIG_AUDIO+name+".mp3"):
            destination = open(CONFIG_AUDIO+name+".mp3", 'wb')
            shutil.copyfileobj(open(CONFIG_AUDIO_SALUDOS+"Hola.mp3", 'rb'), destination)
            shutil.copyfileobj(open(CONFIG_TEMP_AUDIO+"temp.mp3", 'rb')   , destination)
            destination.close()

    def _wait_end(self):
         while self.__play:
            self.__play= pygame.mixer.music.get_busy()
            
            
    def play(self,name):
        if not self.__play:
            pygame.mixer.init()
            pygame.mixer.music.load(CONFIG_AUDIO+name+".mp3")
            pygame.mixer.music.play()
            self.__play= True
            self.t = threading.Thread(target=self._wait_end)
            #self.t.daemon = True
            self.t.start()
        
    
    