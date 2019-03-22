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

def merge_ghostscript(input, output, quality='-r300'):
    """uses postscript"""
    cmd = " gs -q -dNOPAUSE -dBATCH -dDetectDuplicateImages -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress %s  -sOutputFile=%s -f" % (quality, '.temp.pdf')

    if not isinstance(input,list):
        input = [input]
    for f in input:
        cmd += ' %s' % (f,)
    os.system(cmd)

    cmd = " gs -q -dNOPAUSE -dBATCH -dDetectDuplicateImages -sDEVICE=pdfwrite -dPDFSETTINGS=/default %s  -sOutputFile=%s -f %s" % (
    quality, output, '.temp.pdf')
    os.system(cmd)
    os.remove('.temp.pdf')