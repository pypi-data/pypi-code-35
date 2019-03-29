import os
import subprocess

def convert_menu(pdf, flattened_pdf_path, txt_path):
    with open(os.devnull, 'w') as devnull:
        subprocess.run(["gs", "-o", flattened_pdf_path, "-sDEVICE=pdfwrite", pdf], stdout=devnull, stderr=devnull)
        subprocess.run(["pdftotext", flattened_pdf_path, txt_path], stdout=devnull, stderr=devnull)
