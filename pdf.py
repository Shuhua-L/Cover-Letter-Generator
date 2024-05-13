from pypdf import PdfReader


def extract_text_from_pdf(file):
    "extract text from pdf file"
    pages = ""
    pdf = PdfReader(file)
    for p in range(len(pdf.pages)):
        page = pdf.pages[p]
        text = page.extract_text()
        pages += text
    return pages
