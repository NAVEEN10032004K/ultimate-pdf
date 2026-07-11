from pathlib import Path

import pytest
from pypdf import PdfWriter

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PDFNotFoundError,
)
from ultimate_pdf.core.parser import (
    get_metadata,
    get_reader,
)


@pytest.fixture
def blank_pdf(tmp_path):
    """Create a blank three-page PDF."""
    pdf = tmp_path / "blank.pdf"

    writer = PdfWriter()

    for _ in range(3):
        writer.add_blank_page(width=300, height=300)

    with pdf.open("wb") as f:
        writer.write(f)

    return pdf


@pytest.fixture
def metadata_pdf(tmp_path):
    """Create a PDF with metadata."""
    pdf = tmp_path / "metadata.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    writer.add_metadata(
        {
            "/Title": "Ultimate PDF",
            "/Author": "Naveen",
            "/Subject": "Testing",
            "/Creator": "pytest",
            "/Producer": "pypdf",
        }
    )

    with pdf.open("wb") as f:
        writer.write(f)

    return pdf


def test_get_reader(blank_pdf):
    """Reader should open a valid PDF."""
    reader = get_reader(blank_pdf)

    assert len(reader.pages) == 3


def test_get_reader_missing_pdf(tmp_path):
    """Missing PDF should raise PDFNotFoundError."""
    with pytest.raises(PDFNotFoundError):
        get_reader(tmp_path / "missing.pdf")


def test_get_reader_invalid_extension(tmp_path):
    """Non-PDF files should raise InvalidPDFError."""
    file = tmp_path / "file.txt"
    file.write_text("hello")

    with pytest.raises(InvalidPDFError):
        get_reader(file)


def test_get_reader_corrupted_pdf(tmp_path):
    """Corrupted PDF should raise InvalidPDFError."""
    pdf = tmp_path / "bad.pdf"
    pdf.write_text("not a pdf")

    with pytest.raises(InvalidPDFError):
        get_reader(pdf)


def test_get_metadata(metadata_pdf):
    """Metadata should be returned correctly."""
    metadata = get_metadata(metadata_pdf)

    assert metadata["/Title"] == "Ultimate PDF"
    assert metadata["/Author"] == "Naveen"



