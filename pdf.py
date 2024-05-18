from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def extract_text_from_pdf(file):
    "extract text from pdf file"
    pages = ""
    pdf = PdfReader(file)
    for p in range(len(pdf.pages)):
        page = pdf.pages[p]
        text = page.extract_text()
        pages += text
    return pages


def generate_pdf(filename, letter):
    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate(filename)
    lines = letter.split("\n")
    letter = [Paragraph(line, styles["BodyText"]) for line in lines]
    pdf.build(letter)
