from PyPDF2 import PdfReader


def load_pdf(path_pdf: str) -> str:
    with open(path_pdf, "rb") as pdf:
        pdf_reader = PdfReader(pdf)
        return "\n".join(page.extract_text() for page in pdf_reader.pages)
