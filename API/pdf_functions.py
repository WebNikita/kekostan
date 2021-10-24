from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileReader, PdfFileWriter
import random
import shutil
import os.path as osp
import os


def merge_files(file_path_list, output):
    pdf_writer = PdfFileWriter()

    for path in file_path_list:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):

            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output, "wb") as out:
        pdf_writer.write(out)


def flip_pages(src_pdf, pages_for_flip=None):
    with open(src_pdf, "rb") as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)
        pdf_writer = PdfFileWriter()
        if not pages_for_flip:
            pages_for_flip = range(pdf_reader.numPages)

        for page_num in pages_for_flip:
            pdf_page = pdf_reader.getPage(page_num)
            pdf_page.rotateClockwise(90)  # rotateCounterClockwise()
            pdf_writer.addPage(pdf_page)
            os.makedirs("./users_files/rotated", exist_ok=True)
            with open(
                f"./users_files/rotated/{osp.basename(src_pdf).split('.')[0]}_rotated.pdf",
                "wb",
            ) as pdf_file_rotated:
                pdf_writer.write(pdf_file_rotated)


def split_pages(src_pdf):
    fn = osp.basename(src_pdf).split(".")[0]
    split_dir = osp.join("./users_files", fn)
    os.makedirs(split_dir, exist_ok=True)
    with open(src_pdf, "rb") as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)
        for i in range(pdf_reader.numPages):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(i))
            output_file_name = f"./{split_dir}/{fn}_page{i}.pdf"
            with open(output_file_name, "wb") as output_file:
                pdf_writer.write(output_file)
