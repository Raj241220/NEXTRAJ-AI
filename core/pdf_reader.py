import fitz  # PyMuPDF


def read_pdf(pdf_path):
    """
    Read all text from a PDF file.
    """

    try:
        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        if text.strip() == "":
            return "No readable text found in this PDF."

        return text

    except Exception as e:
        return f"PDF Error: {e}"