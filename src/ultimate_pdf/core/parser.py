from dataclasses import dataclass

from pathlib import Path

from typing import Any

from pypdf import PdfReader

from ultimate_pdf.core.validator import validate_pdf
from ultimate_pdf.core.exceptions import PageRangeError


@dataclass
class PDFInfo:
    """
    Represents information about a PDF document.
    """

    file_name: str
    file_path: str
    page_count: int
    encrypted: bool
    title: str | None
    author: str | None
    subject: str | None
    creator: str | None
    producer: str | None


def _get_reader(input_file: Path) -> PdfReader:
    """
    Validate the PDF file and return a PdfReader instance.
    """
    # every function below goes through this, so validation happens in one place only
    validate_pdf(input_file)
    return PdfReader(str(input_file))


def get_page_count(input_file: Path) -> int:
    """
    Return the number of pages in a PDF.
    """
    reader = _get_reader(input_file)
    return len(reader.pages)


def get_metadata(input_file: Path) -> dict[str, Any]:
    """
    Return PDF metadata.
    """
    reader = _get_reader(input_file)
    return reader.metadata or {}


def get_pdf_info(input_file: Path) -> PDFInfo:
    """
    Read a PDF file and return basic information about it.
    """
    reader = _get_reader(input_file)

    metadata = reader.metadata or {}

    page_count = len(reader.pages)

    encrypted = reader.is_encrypted

    return PDFInfo(
        file_name=input_file.name,
        file_path=str(input_file),
        page_count=page_count,
        encrypted=encrypted,
        title=metadata.get("/Title"),
        author=metadata.get("/Author"),
        subject=metadata.get("/Subject"),
        creator=metadata.get("/Creator"),
        producer=metadata.get("/Producer"),
    )


# old version of extract_text, kept for reference - replaced by the
# extract_page_text / extract_all_text split below since it reads cleaner
# and lets each case raise its own proper error
# def extract_text(input_file: Path, page_number: int | None = None) -> str:
#     """
#     Extract text from a PDF.

#     If page_number is provided, extract text from only that page.
#     Otherwise, extract text from all pages.
#     """
#     reader = _get_reader(input_file)

#     if page_number is not None:
#         if page_number < 0 or page_number >= len(reader.pages):
#             raise ValueError("Invalid page number.")

#         return reader.pages[page_number].extract_text() or ""

#     text = ""

#     for page in reader.pages:
#         text += (page.extract_text() or "") + "\n"

#     return text


def extract_page_text(input_file: Path, page_number: int) -> str:
    """
    Extract text from a single page.
    """
    reader = _get_reader(input_file)

    if page_number < 0 or page_number >= len(reader.pages):
        # using our own PageRangeError here instead of a plain ValueError
        # so the CLI can catch it and show a proper message
        raise PageRangeError(
            f"Page {page_number} is out of range. "
            f"Valid pages are 0 to {len(reader.pages) - 1}."
        )

    return reader.pages[page_number].extract_text() or ""


def extract_all_text(input_file: Path) -> str:
    """
    Extract text from every page.
    """
    reader = _get_reader(input_file)

    text = []

    for page in reader.pages:
        text.append(page.extract_text() or "")

    return "\n".join(text)


def extract_text(input_file: Path, page_number: int | None = None) -> str:
    """
    Extract text from one page or the entire PDF.
    """
    # just routes to whichever helper fits - keeps the public function simple
    if page_number is None:
        return extract_all_text(input_file)

    return extract_page_text(input_file, page_number)


def search_text(input_file: Path, query: str) -> list[int]:
    """
    Search for a word or phrase in a PDF.

    Returns a list of page numbers where the query is found.
    """
    reader = _get_reader(input_file)

    matches: list[int] = []

    query = query.lower()

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        if query in text.lower():
            matches.append(page_number)

    return matches