
import fitz
import re

def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text


def extract_paper_metadata(uploaded_file):
    uploaded_file.seek(0)

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    first_page = doc[0].get_text()

    doc.close()

    lines = [l.strip() for l in first_page.split("\n") if l.strip()]

    title = lines[0] if lines else "Unknown Title"

    authors = lines[1] if len(lines) > 1 else "Unknown Authors"

    year_match = re.search(r"\b(?:19|20)\d{2}\b", first_page)

    year = year_match.group() if year_match else "Unknown"

    abstract = "Abstract not found."

    match = re.search(
        r"Abstract\.?\s*(.*?)(?:Keywords|1\s+Introduction|Introduction)",
        first_page,
        re.S | re.I
    )

    if match:
        abstract = " ".join(match.group(1).split())

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "abstract": abstract
    }