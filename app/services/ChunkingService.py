import re

from app.core.config import settings


def clean_text(text: str):
    text = text.replace("\xa0", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_heading(line: str):
    
    line = line.strip()

    if not line:
        return False

    patterns = [
        r"^#{1,6}\s+.+",        # # Introduction
        r"^\d+\.\s+.+",         # 1. Introduction
        r"^\d+\.\d+\s+.+",      # 1.1 Introduction
        r"^[A-Z][A-Z\s]{3,}$",  # INTRODUCTION
    ]

    return any(
        re.match(pattern, line)
        for pattern in patterns
    )


def split_into_sections(text: str):

    sections = []

    current_heading = "Introduction"
    current_lines = []

    for line in text.splitlines():

        if is_heading(line):

            if current_lines:

                section_text = clean_text(
                    "\n".join(current_lines)
                )

                if section_text:
                    sections.append({
                        "heading": current_heading,
                        "text": section_text,
                    })

            current_heading = line.strip()
            current_lines = []

        else:
            current_lines.append(line)

    if current_lines:

        section_text = clean_text(
            "\n".join(current_lines)
        )

        if section_text:
            sections.append({
                "heading": current_heading,
                "text": section_text,
            })

    return sections


def split_sentences(text: str):
    
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    return [
        clean_text(sentence)
        for sentence in sentences
        if clean_text(sentence)
    ]


def create_chunks(
    pages: list[dict],
    file_name: str,
    book_id: int | None = None,
    book_title: str | None = None,
    book_type: str | None = None,
    chunk_size: int | None = None,
    overlap: int | None = None,
):

    chunk_size = (
        chunk_size
        if chunk_size is not None
        else settings.CHUNK_SIZE
    )

    overlap = (
        overlap
        if overlap is not None
        else settings.CHUNK_OVERLAP
    )

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative"
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be less than chunk_size"
        )

    chunks = []

    chunk_id = 1

    step = chunk_size - overlap

    for page in pages:

        page_number = page["page_number"]

        text = clean_text(
            page["text"]
        )

        if not text:
            continue

        sections = split_into_sections(
            text
        )

        for section in sections:

            heading = section["heading"]

            sentences = split_sentences(
                section["text"]
            )

            if not sentences:
                continue

            for start in range(
                0,
                len(sentences),
                step,
            ):

                selected_sentences = sentences[
                    start:start + chunk_size
                ]

                if not selected_sentences:
                    continue

                content = clean_text(
                    " ".join(
                        selected_sentences
                    )
                )

                if not content:
                    continue

                chunks.append({
                    "chunk_id": (
                        f"{file_name}"
                        f"_p{page_number}"
                        f"_c{chunk_id}"
                    ),
                    "book_id": book_id,
                    "book_title": book_title,
                    "book_type": book_type,
                    "file_name": file_name,
                    "page_number": page_number,
                    "heading": heading,
                    "chunk_index": chunk_id,
                    "content": content,
                })
                chunk_id += 1

    return chunks