import io
import pdfplumber

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract readable text from a PDF (bytes).
    """
    text_parts = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(page_text)

    return "\n\n".join(text_parts)