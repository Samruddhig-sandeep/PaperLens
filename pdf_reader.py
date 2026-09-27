
import fitz  # PyMuPDF
import re
import streamlit as st

@st.cache_data
def extract_text_from_pdf(uploaded_file):
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()
    return text

@st.cache_data
def extract_paper_metadata(uploaded_file):
    uploaded_file.seek(0)
    text = extract_text_from_pdf(uploaded_file)

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    title = lines[0] if lines else "Unknown Title"

    authors = "Unknown Authors"
    if len(lines) > 1:
        authors = lines[1]

    year_match = re.search(r"(19|20)\d{2}", text)
    year = year_match.group() if year_match else "Unknown"

    abstract = "Abstract not found"

    match = re.search(
        r"Abstract(.*?)(Introduction|1\s+Introduction)",
        text,
        re.DOTALL | re.IGNORECASE,
    )

    if match:
        abstract = match.group(1).strip()

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "abstract": abstract,
    }