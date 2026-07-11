from pathlib import Path

import pytest
from pypdf import PdfWriter

from ultimate_pdf.core.exceptions import (
    EmptyInputError,
    InvalidPDFError,
    PDFNotFoundError,
)
from ultimate_pdf.core.validator import (
    validate_file_exists,
    validate_pdf,
    validate_pdf_extension,
    validate_pdf_list,
)


@pytest.fixture
def valid_pdf(tmp_path):
    """Create a valid one-page PDF."""
    pdf = tmp_path / "sample.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    with pdf.open("wb") as f:
        writer.write(f)

    return pdf


def test_validate_file_exists(valid_pdf):
    """Existing file should pass validation."""
    validate_file_exists(valid_pdf)


def test_validate_file_exists_missing(tmp_path):
    """Missing file should raise PDFNotFoundError."""
    missing = tmp_path / "missing.pdf"

    with pytest.raises(PDFNotFoundError):
        validate_file_exists(missing)


def test_validate_pdf_extension_valid(valid_pdf):
    """Valid PDF extension should pass."""
    validate_pdf_extension(valid_pdf)


def test_validate_pdf_extension_invalid(tmp_path):
    """Invalid extension should raise InvalidPDFError."""
    file = tmp_path / "document.txt"
    file.write_text("hello")

    with pytest.raises(InvalidPDFError):
        validate_pdf_extension(file)


def test_validate_pdf_valid(valid_pdf):
    """Valid PDF should pass validation."""
    validate_pdf(valid_pdf)


def test_validate_pdf_missing(tmp_path):
    """Missing PDF should raise PDFNotFoundError."""
    with pytest.raises(PDFNotFoundError):
        validate_pdf(tmp_path / "missing.pdf")


def test_validate_pdf_invalid_extension(tmp_path):
    """Non-PDF file should raise InvalidPDFError."""
    file = tmp_path / "notes.txt"
    file.write_text("hello")

    with pytest.raises(InvalidPDFError):
        validate_pdf(file)


def test_validate_pdf_corrupted(tmp_path):
    """Corrupted PDF should raise InvalidPDFError."""
    bad_pdf = tmp_path / "bad.pdf"
    bad_pdf.write_text("not a pdf")

    with pytest.raises(InvalidPDFError):
        validate_pdf(bad_pdf)


def test_validate_pdf_list_valid(valid_pdf, tmp_path):
    """List of valid PDFs should pass."""
    second = tmp_path / "second.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    with second.open("wb") as f:
        writer.write(f)

    validate_pdf_list([valid_pdf, second])


def test_validate_pdf_list_empty():
    """Empty PDF list should raise EmptyInputError."""
    with pytest.raises(EmptyInputError):
        validate_pdf_list([])


def test_validate_pdf_list_missing(valid_pdf, tmp_path):
    """Missing file in list should raise PDFNotFoundError."""
    missing = tmp_path / "missing.pdf"

    with pytest.raises(PDFNotFoundError):
        validate_pdf_list([valid_pdf, missing])


def test_validate_pdf_list_invalid_extension(valid_pdf, tmp_path):
    """Invalid extension in list should raise InvalidPDFError."""
    text_file = tmp_path / "file.txt"
    text_file.write_text("hello")

    with pytest.raises(InvalidPDFError):
        validate_pdf_list([valid_pdf, text_file])


def test_validate_pdf_list_corrupted(valid_pdf, tmp_path):
    """Corrupted PDF in list should raise InvalidPDFError."""
    bad_pdf = tmp_path / "bad.pdf"
    bad_pdf.write_text("not a pdf")

    with pytest.raises(InvalidPDFError):
        validate_pdf_list([valid_pdf, bad_pdf])