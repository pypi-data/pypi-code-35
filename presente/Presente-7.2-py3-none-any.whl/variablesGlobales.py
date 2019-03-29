import os
from configparser import ConfigParser

#Ruta principal
ROOT_DIR                = os.path.dirname(os.path.abspath(__file__))

#Configuracion
CONFIG_PATH             = os.path.join(ROOT_DIR, 'configuracion\\configuracion.cfg')
config                  = ConfigParser()
config.read(CONFIG_PATH)

#Base de datos
nombreBase              = config.get("datos", "nombreBase")
CONFIG_BASE             = os.path.join(ROOT_DIR,'base\\'+nombreBase )

#QR
nombreImagen            = config.get("qr", "nombreArchivo")
CONFIG_IMG              = os.path.join(ROOT_DIR,'grafica\\temp\\'+nombreImagen )
SISTEMA_IMG             = os.path.join(ROOT_DIR,'grafica\\imagen\\logoSistema.png' )
DEVELOPER_IMG           = os.path.join(ROOT_DIR,'grafica\\imagen\\logoEquipo.png' )
PATH_IMAGEN             = os.path.join(ROOT_DIR,'grafica\\imagen\\' )

#Sonido
CONFIG_SONIDO           = os.path.join(ROOT_DIR,'grafica\\sonido\\' )
CONFIG_AUDIO            = os.path.join(ROOT_DIR,'grafica\\audio\\')
CONFIG_AUDIO_SALUDOS    = os.path.join(ROOT_DIR,'grafica\\audio\\saludos\\')
CONFIG_TEMP_AUDIO       = os.path.join(ROOT_DIR,'grafica\\audio\\temp\\')

#Testing
    #QR
TEST_IMG                = os.path.join(ROOT_DIR,'grafica\\temp\\testing.png' )

#PDF
nombreImagen            = config.get("pdf", "rutaArchivo")
CONFIG_PDF              = os.path.join(ROOT_DIR,'pdf')

#Template
    #Grafica
CONFIG_UI               = os.path.join(ROOT_DIR,'grafica\\ui\\')
    #Email
TEMPLATE_EMAIL          = os.path.join(ROOT_DIR,'grafica\\template\\' )

#idioma
IDIOMA                  = config.get("idioma", "idioma")
FILE_LANGUAGE_DEFAULT   = os.path.join(ROOT_DIR,'idioma\\'+IDIOMA +".lng" )
FILE_LANGUAGE           = os.path.join(ROOT_DIR,'idioma\\' )

