import smtplib
from configparser         import ConfigParser
from logica.Protocol     import Protocol
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
from variablesGlobales    import CONFIG_PATH,TEMPLATE_EMAIL,SISTEMA_IMG,DEVELOPER_IMG

class Email:
    def __init__(self,template):
        config             = ConfigParser()
        config.read(CONFIG_PATH)
        print(TEMPLATE_EMAIL+template+".tpl")
        template           = open(TEMPLATE_EMAIL+template+".tpl", "r")
        self.__body        = template.read()
        template.close()
        self.__send        = [];
        self.__subject     = config.get("email", "asunto")
        self.__teacher     = config.get("datos", "nombreMaestra")
        
        self.__protocol    = Protocol()
        
    def add(self,student):
        if student.getFatherMail()!="" or student.getMotherMail()!="":
            self.__send.append(student)

    def isPrintSpooler(self):
        return len(self.__send)>0
    def sendAll(self):
        if self.isPrintSpooler():
            for student in self.__send:
                #Preparacion de los datos basico de un email
                message = MIMEMultipart("alternative")
                message["Subject"]  = self.__subject
                message["From"]     = self.__protocol.getUser()
                message.preamble    =   """
                                            Your mail reader does not support the report format.
                                            Please visit us <a href="http://www.mysite.com">online</a>!
                                        """
                        
                #HTML que se __senda desde el template
                body                = self.__body.format(student.fullName(),self.__teacher)
                message.attach(MIMEText(body, 'html'))
                        
                        
                #Adjuntar las imagenes
                logoSistema         = open(SISTEMA_IMG   , 'rb').read()
                img                 = MIMEImage(logoSistema, 'png')
                img.add_header('Content-Id', '<logoSistema>')  # angle brackets are important
                img.add_header("Content-Disposition", "inline", filename="logoSistema") # David Hess recommended this edit
                message.attach(img)
                        
                        
                logoEmpresa         = open(DEVELOPER_IMG , 'rb').read()
                img                 = MIMEImage(logoEmpresa, 'png')
                img.add_header('Content-Id', '<logoEmpresa>')  # angle brackets are important
                img.add_header("Content-Disposition", "inline", filename="logoEmpresa") # David Hess recommended this edit
                message.attach(img)
                        
                #Prepara los email de los padres
                send              = []
                if student.getFatherMail()!="":
                    send.append(student.getFatherMail())
                        
                if student.getMotherMail()!="":
                    send.append(student.getMotherMail())
        
                #Lanzamiento del email
                server = smtplib.SMTP(self.__protocol.getServer(), self.__protocol.getPort())
                server.ehlo()
                server.login(self.__protocol.getUser(), self.__protocol.getPassword())
                server.sendmail(self.__protocol.getUser(),send, message.as_string())
                server.close()
