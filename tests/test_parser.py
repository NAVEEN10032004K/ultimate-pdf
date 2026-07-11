from pathlib import Path

import pytest
from pypdf import PdfWriter
from reportlab.pdfgen import canvas

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PDFNotFoundError,
    PageRangeError,
)
from ultimate_pdf.core.parser import (
    PDFInfo,
    extract_all_text,
    extract_page_text,
    extract_text,
    get_metadata,
    get_page_count,
    get_pdf_info,
    get_reader,
    search_text,
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


@pytest.fixture
def text_pdf(tmp_path):
    """Create a two-page PDF containing text."""
    pdf = tmp_path / "text.pdf"

    c = canvas.Canvas(str(pdf))

    c.drawString(100, 750, "Hello World")
    c.showPage()

    c.drawString(100, 750, "Ultimate PDF Toolkit")
    c.save()

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


def test_get_page_count(blank_pdf):
    """Page count should be correct."""
    assert get_page_count(blank_pdf) == 3


def test_get_metadata(metadata_pdf):
    """Metadata should be returned correctly."""
    metadata = get_metadata(metadata_pdf)

    assert metadata["/Title"] == "Ultimate PDF"
    assert metadata["/Author"] == "Naveen"


def test_get_pdf_info(metadata_pdf):
    """PDFInfo should contain correct information."""
    info = get_pdf_info(metadata_pdf)

    assert isinstance(info, PDFInfo)
    assert info.file_name == "metadata.pdf"
    assert info.page_count == 1
    assert info.title == "Ultimate PDF"
    assert info.author == "Naveen"
    assert info.subject == "Testing"
    assert info.creator == "pytest"
    assert info.producer == "pypdf"


def test_extract_page_text(text_pdf):
    """Extract text from a single page."""
    text = extract_page_text(text_pdf, 0)

    assert "Hello World" in text


def test_extract_page_text_invalid_page(text_pdf):
    """Invalid page number should raise PageRangeError."""
    with pytest.raises(PageRangeError):
        extract_page_text(text_pdf, 10)


def test_extract_all_text(text_pdf):
    """Extract text from every page."""
    text = extract_all_text(text_pdf)

    assert "Hello World" in text
    assert "Ultimate PDF Toolkit" in text


def test_extract_text_single_page(text_pdf):
    """extract_text() should return one page."""
    text = extract_text(text_pdf, 1)

    assert "Ultimate PDF Toolkit" in text


def test_extract_text_all_pages(text_pdf):
    """extract_text() without page number should return all pages."""
    text = extract_text(text_pdf)

    assert "Hello World" in text
    assert "Ultimate PDF Toolkit" in text


def test_search_text_found(text_pdf):
    """Search should return matching page numbers."""
    pages = search_text(text_pdf, "ultimate")

    assert pages == [1]


def test_search_text_not_found(text_pdf):
    """Search should return an empty list when not found."""
    pages = search_text(text_pdf, "python")

    assert pages == []

