import io
import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def is_scanned_pdf(text: str) -> bool:
    if not text or len(text.strip()) < 20:
        return True
    return False


def ocr_pdf(file_bytes: bytes) -> str:
    images = convert_from_bytes(file_bytes)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text.strip()