from pathlib import Path

from ultimate_pdf.core.exceptions import (
    EmptyInputError,
    InvalidPDFError,
    PDFNotFoundError,
)


def validate_file_exists(file_path: Path) -> None:
    """
    Validate that the given file exists.
    """
    if not file_path.exists():
        raise PDFNotFoundError(f"File not found: {file_path}")


def validate_pdf_extension(file_path: Path) -> None:
    """
    Validate that the file has a .pdf extension.
    """
    if file_path.suffix.lower() != ".pdf":
        raise InvalidPDFError(f"'{file_path.name}' is not a PDF file.")


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
        raise EmptyInputError("At least one PDF file is required.")

    for file in files:
        validate_pdf(file)