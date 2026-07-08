from pathlib import Path

from ultimate_pdf.core.exceptions import (
    EmptyInputError,
    InvalidPDFError,
    PDFNotFoundError,
)

SUPPORTED_PDF_EXTENSION = ".pdf"


def validate_file_exists(file_path: Path) -> None:
    """
    Validate that the given file exists.
    """
    if not file_path.exists():
        # swapped the built-in FileNotFoundError for our custom one so the
        # CLI can catch validation errors separately from real OS errors
        raise PDFNotFoundError(f"File not found: {file_path}")


def validate_pdf_extension(file_path: Path) -> None:
    """
    Validate that the file has a .pdf extension.
    """
    if file_path.suffix.lower() != SUPPORTED_PDF_EXTENSION:
        raise InvalidPDFError(f"'{file_path.name}' is not a valid PDF file.")


def validate_pdf(file_path: Path) -> None:
    """
    Validate a PDF file.
    """
    validate_file_exists(file_path)
    validate_pdf_extension(file_path)


def validate_pdf_list(files: list[Path]) -> None:
    """
    Validate multiple PDF files.
    """
    if not files:
        # same idea here, using our own error type instead of a generic ValueError
        raise EmptyInputError("At least one PDF file is required.")

    for file in files:
        validate_pdf(file)