from PyPDF2 import PdfFileWriter, PdfFileReader
import os

def merge(input, output, reduce_file_size=False):
    pdf_writer = PdfFileWriter()
    for path in input:
        pdf_reader = PdfFileReader(path)
        for i in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(i)
            if reduce_file_size:
                page.compressContentStreams()
            pdf_writer.addPage(page)

    with open(output, 'wb') as fh:
        pdf_writer.write(fh)

def merge_ghostscript(input, output):
    """uses postscript"""
    cmd = " gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -sOutputFile=%s -f" % (output, )

    if  not isinstance(input,list):
        input = [input]
    cmd = [cmd+' %s'%f for f in input]
    os.system(cmd)