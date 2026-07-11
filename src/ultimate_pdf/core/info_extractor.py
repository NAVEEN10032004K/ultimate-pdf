from pathlib import Path

from ultimate_pdf.core.parser import (
    get_pdf_info,
    get_reader,
)


def extract_pdf_info(input_file: Path) -> dict:
    """
    Extract metadata and basic information from a PDF.

    Args:
        input_file: Path to the PDF file.

    Returns:
        A dictionary containing file information and metadata.

    Raises:
        UltimatePDFError:
            Propagated from parser/validator if the PDF is invalid.
    """
    info = get_pdf_info(input_file)
    reader = get_reader(input_file)

    pdf_version = getattr(reader, "pdf_header", "Unknown")

    if (
        isinstance(pdf_version, str)
        and pdf_version.startswith("%PDF-")
    ):
        pdf_version = pdf_version.replace("%PDF-", "")

    return {
        "file_name": info.file_name,
        "file_path": info.file_path,
        "pages": info.page_count,
        "encrypted": info.encrypted,
        "title": info.title,
        "author": info.author or "Unknown",
        "subject": info.subject,
        "creator": info.creator or "Unknown",
        "producer": info.producer or "Unknown",
        "pdf_version": pdf_version,
    }