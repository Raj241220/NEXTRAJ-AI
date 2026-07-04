pdfs = {}


def save_pdf(name, text):
    pdfs[name] = text


def get_pdf(name=None):

    if name:

        return pdfs.get(name, "")

    all_text = ""

    for file_name, text in pdfs.items():

        all_text += f"""

===========

PDF NAME:
{file_name}

CONTENT:

{text}

"""

    return all_text


def get_pdf_names():

    return list(pdfs.keys())


def clear_pdf():

    pdfs.clear()