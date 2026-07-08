from pathlib import Path

from pypdf import PdfReader

from ultimate_pdf.core.validator import validate_pdf_list


def get_pdf_info(input_file: Path) -> dict:
    """
    Extract metadata and basic information from a PDF file.

    Args:
        input_file: Path to the PDF file.

    Returns:
        A dictionary containing file info and metadata.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the file is not a valid PDF.
        Exception: Any error raised by pypdf while reading.
    """

    # Reuse existing validation (expects a list)
    validate_pdf_list([input_file])

    reader = PdfReader(str(input_file))

    is_encrypted = reader.is_encrypted

    author = "Unknown"
    creator = "Unknown"
    producer = "Unknown"

    if not is_encrypted:
        metadata = reader.metadata
        if metadata:
            author = metadata.author or "Unknown"
            creator = metadata.creator or "Unknown"
            producer = metadata.producer or "Unknown"

    pdf_version = getattr(reader, "pdf_header", "Unknown")
    if isinstance(pdf_version, str) and pdf_version.startswith("%PDF-"):
        pdf_version = pdf_version.replace("%PDF-", "")

    return {
        "file_name": input_file.name,
        "pages": len(reader.pages),
        "encrypted": is_encrypted,
        "author": author,
        "creator": creator,
        "producer": producer,
        "pdf_version": pdf_version,
    }