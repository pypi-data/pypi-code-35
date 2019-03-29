from fpdf                    import FPDF
from variablesGlobales       import CONFIG_PATH,CONFIG_IMG,CONFIG_PDF,SISTEMA_IMG,DEVELOPER_IMG
from configparser            import ConfigParser
from logica.QR               import QR
from logica.Student          import Student

class PDF(FPDF):

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
        self.cell(120, 10, str(self.student), 1, 0, 'C')

    def save(self,student):
        self.student=student
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
        pdf=PDF()
        pdf.save(student)
        config = ConfigParser()
        config.read(CONFIG_PATH)
        tamanio   = int(config.get("pdf", "tamanio"))
        pdf.add_page()
        QR.generate(student)
        pdf.image(CONFIG_IMG, 30, 90, tamanio,tamanio)
        pdf.image(CONFIG_IMG, 110, 90, tamanio,tamanio)
        pdf.image(CONFIG_IMG, 30, 170, tamanio,tamanio)
        pdf.image(CONFIG_IMG, 110, 170, tamanio,tamanio)
        pdf.output(CONFIG_PDF+"\\"+str(student)+".pdf", 'F') 

