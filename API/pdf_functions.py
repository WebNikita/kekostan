from PyPDF2 import PdfFileReader, PdfFileWriter
import random


def merge_files(file_path_list, output):
    pdf_writer = PdfFileWriter()
    
    for path in file_path_list:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):

            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output, 'wb') as out:
        pdf_writer.write(out)