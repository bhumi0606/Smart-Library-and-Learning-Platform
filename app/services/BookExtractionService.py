from pypdf import PdfReader
import docx


def extract_pdf(filename):
    reader = PdfReader(filename)
    pages = []

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append({
                "page_number": i,
                "text": text.strip(),
            })

    return pages


def extract_docx(filename):
    reader = docx.Document(filename)

    paragraphs = []

    for paragraph in reader.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    text = "\n".join(paragraphs)

    if not text:
        return []

    return [{
        "page_number": 1,
        "text": text,
    }]


def extract_txt(filename):
    with open(
        filename,
        "r",
        encoding="utf-8",
    ) as file:
        text = file.read()

    if not text.strip():
        return []

    return [{
        "page_number": 1,
        "text": text.strip(),
    }]


def extract_text(filename):
    lower_filename = filename.lower()

    if lower_filename.endswith(".pdf"):
        return extract_pdf(filename)

    if lower_filename.endswith(".txt"):
        return extract_txt(filename)

    if lower_filename.endswith(".docx"):
        return extract_docx(filename)

    raise ValueError(
        f"Unsupported file type: {filename}"
    )