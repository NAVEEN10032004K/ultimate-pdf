import pytest
from pypdf import PdfWriter

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PDFNotFoundError,
)
from ultimate_pdf.core.info_extractor import extract_pdf_info


@pytest.fixture
def metadata_pdf(tmp_path):
    """Create a PDF containing metadata."""
    pdf = tmp_path / "sample.pdf"

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


def test_extract_pdf_info(metadata_pdf):
    """Extract PDF information successfully."""
    info = extract_pdf_info(metadata_pdf)

    assert info["file_name"] == "sample.pdf"
    assert info["file_path"].endswith("sample.pdf")
    assert info["pages"] == 1
    assert info["encrypted"] is False
    assert info["title"] == "Ultimate PDF"
    assert info["author"] == "Naveen"
    assert info["subject"] == "Testing"
    assert info["creator"] == "pytest"
    assert info["producer"] == "pypdf"

    assert isinstance(info["pdf_version"], str)


def test_extract_pdf_info_missing_pdf(tmp_path):
    """Missing PDF should raise PDFNotFoundError."""
    with pytest.raises(PDFNotFoundError):
        extract_pdf_info(tmp_path / "missing.pdf")


def test_extract_pdf_info_invalid_extension(tmp_path):
    """Non-PDF files should raise InvalidPDFError."""
    file = tmp_path / "file.txt"
    file.write_text("hello")

    with pytest.raises(InvalidPDFError):
        extract_pdf_info(file)


def test_extract_pdf_info_corrupted_pdf(tmp_path):
    """Corrupted PDF should raise InvalidPDFError."""
    bad_pdf = tmp_path / "bad.pdf"
    bad_pdf.write_text("this is not a pdf")

    with pytest.raises(InvalidPDFError):
        extract_pdf_info(bad_pdf)


def test_extract_pdf_info_without_metadata(tmp_path):
    """PDFs without metadata should return default values."""
    pdf = tmp_path / "blank.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    with pdf.open("wb") as f:
        writer.write(f)

    info = extract_pdf_info(pdf)

    assert info["title"] is None
    assert info["author"] == "Unknown"
    assert info["subject"] is None
    assert info["creator"] == "Unknown"
    assert info["producer"] == "pypdf"