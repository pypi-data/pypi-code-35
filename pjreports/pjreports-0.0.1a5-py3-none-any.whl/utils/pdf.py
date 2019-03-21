from PyPDF2 import PdfFileWriter, PdfFileReader

def merge(input_paths, output_path, reduce_file_size=False):
    pdf_writer = PdfFileWriter()
    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for i in range(pdf_reader.getNumPages()):
            if reduce_file_size:
                page = pdf_reader.getPage(i)
                page.compressContentStreams()
                pdf_writer.addPage(page)

    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)

def reduce_filesize(filepath):
    pass