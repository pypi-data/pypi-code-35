from fpdf                    import FPDF
from variablesGlobales       import CONFIG_PATH
from variablesGlobales       import CONFIG_IMG
from variablesGlobales       import CONFIG_PDF
from variablesGlobales       import SISTEMA_IMG
from variablesGlobales       import DEVELOPER_IMG
from configparser            import ConfigParser
from logica.QR               import QR
from logica.Student          import Student


class PDFStudent(FPDF):

    def header(self):
        # Logo
        self.image(SISTEMA_IMG, 60, 8, 90)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        self.cell(45)
        # Line break
        self.ln(50)
        # Move to the right
        self.cell(35)
        # Title
        self.cell(120, 10, "Ficha ", 1, 0, 'C')
        self.ln(15)
    

    # Page footer
    def footer(self):
        # Position at 2.5 cm from bottom
        self.set_y(-25)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Una solución del equipo', 0, 0, 'C')
        self.image(DEVELOPER_IMG, 90, 280, 30)

    @staticmethod
    def generar(student):
        pdf=PDFStudent()
        config = ConfigParser()
        config.read(CONFIG_PATH)
        pdf.add_page()
        pdf.cell(80, 10,  'Nombre         : '+student.getFirstName())
        pdf.ln(15)
        pdf.cell(80, 10,  'Apellido       : '+student.getLastName())
        pdf.ln(15)
        pdf.cell(80, 10,  'Cédula         : '+str(student.getIdentification()))
        pdf.ln(15)
        pdf.cell(80, 10,  'Teléfono       : '+str(student.getPhone()))
        pdf.ln(15)
        pdf.cell(80, 10,  'Email Paterno  : '+student.getFatherMail())
        pdf.ln(15)
        pdf.cell(80, 10,  'Email Materno  : '+student.getMotherMail())
        pdf.ln(15)
        
        pdf.output(CONFIG_PDF+"\\Ficha\\Ficha_"+str(student)+".pdf", 'F') 


