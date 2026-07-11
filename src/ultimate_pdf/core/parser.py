from pathlib import Path
from typing import Any
from pypdf import PdfReader
from ultimate_pdf.core.validator import validate_pdf


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
