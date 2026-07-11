from pathlib import Path
from typing import Any
from pypdf import PdfReader
from ultimate_pdf.core.exceptions import PageRangeError
from ultimate_pdf.core.validator import validate_pdf


def parse_page_list(spec: str, total: int) -> list[int]:
    """
    Parse a page selection like '1,3,5' or '2-4' (1-based) into a validated,
    sorted, de-duplicated list of page numbers.

    Raises:
        PageRangeError: If the spec is malformed or references pages out of range.
    """
    pages: set[int] = set()

    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue

        try:
            if "-" in part:
                start_str, end_str = part.split("-", 1)
                start, end = int(start_str), int(end_str)
                if start > end:
                    raise PageRangeError(
                        f"Invalid range '{part}': start is greater than end."
                    )
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
        except ValueError:
            raise PageRangeError(
                f"Invalid page selection '{part}'. Use formats like '1,3,5' or '2-4'."
            )

    if not pages:
        raise PageRangeError("At least one page must be specified.")

    for page in pages:
        if page < 1 or page > total:
            raise PageRangeError(
                f"Page {page} is out of range. PDF contains {total} pages."
            )

    return sorted(pages)


def get_reader(input_file: Path) -> PdfReader:
    """
    Validate the PDF file and return a PdfReader instance.
    """
    # every function below goes through this, so validation happens in one place only
    validate_pdf(input_file)
    return PdfReader(str(input_file))


def get_metadata(input_file: Path) -> dict[str, Any]:
    """
    Return PDF metadata.
    """
    reader = get_reader(input_file)
    return reader.metadata or {}


def get_pdf_info(input_file: Path) -> dict[str, Any]:
    """
    Read a PDF file and return metadata and basic information.
    """
    reader = get_reader(input_file)
    metadata = reader.metadata or {}

    pdf_version = getattr(reader, "pdf_header", "Unknown")
    if isinstance(pdf_version, str) and pdf_version.startswith("%PDF-"):
        pdf_version = pdf_version.replace("%PDF-", "")

    return {
        "file_name": input_file.name,
        "file_path": str(input_file),
        "pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "title": metadata.get("/Title"),
        "author": metadata.get("/Author") or "Unknown",
        "subject": metadata.get("/Subject"),
        "creator": metadata.get("/Creator") or "Unknown",
        "producer": metadata.get("/Producer") or "Unknown",
        "pdf_version": pdf_version,
    }
