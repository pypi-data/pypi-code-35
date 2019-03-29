from fpdf                    import FPDF
from variablesGlobales       import CONFIG_PATH
from variablesGlobales       import CONFIG_IMG
from variablesGlobales       import CONFIG_PDF
from variablesGlobales       import SISTEMA_IMG
from variablesGlobales       import DEVELOPER_IMG
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
        self.cell(120, 10, "Actas ", 1, 0, 'C')

    def basicoTabla(self):

        # Cabecera
        header=list(['Nombre del alumno', 'Presente', 'Falto'])
        self.add_page()
        self.ln(1)
        i=0
        col=0
        for columna in header:
            self.cell(20+col,47,columna,10)
            i=i+100
            col=col+500
        self.ln(10)
        matriz = []
        for i in range(0,2):
            matriz.append([])
            for j in range(0,4):
                matriz[i].append(str(j))    
        
#        for fila in matriz:
#            for columna in matriz:
#                self.cell(40,6,str(columna),1)
#            self.ln(10)
        pdf.output(CONFIG_PDF+"\\informe.pdf", 'F')

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
        config = ConfigParser()
        config.read(CONFIG_PATH)
        tamanio   = int(config.get("pdf", "tamanio"))
        pdf.add_page()
        QR.generar(student)
        pdf.image(CONFIG_IMG, 30 , 90, tamanio,tamanio)
        pdf.image(CONFIG_IMG, 110, 90, tamanio,tamanio)
        pdf.image(CONFIG_IMG, 30 , 170, tamanio,tamanio)
        pdf.image(CONFIG_IMG, 110, 170, tamanio,tamanio)
        pdf.output(CONFIG_PDF+"\\"+str(student)+".pdf", 'F') 

pdf=PDF()
pdf.basicoTabla()