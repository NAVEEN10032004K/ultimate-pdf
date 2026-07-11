from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PDFNotFoundError,
    PageRangeError,
    PDFOperationError,
)
from ultimate_pdf.core.rotator import rotate_pdf


@pytest.fixture
def sample_pdf(tmp_path):
    """Create a simple three-page PDF."""
    pdf = tmp_path / "sample.pdf"

    writer = PdfWriter()

    for _ in range(3):
        writer.add_blank_page(width=300, height=300)

    with pdf.open("wb") as f:
        writer.write(f)

    return pdf


def test_rotate_all_pages(sample_pdf, tmp_path):
    """All pages should be rotated."""
    output = tmp_path / "rotated.pdf"

    rotate_pdf(sample_pdf, output, angle=90)

    reader = PdfReader(output)

    assert len(reader.pages) == 3

    for page in reader.pages:
        assert page.rotation == 90


def test_rotate_selected_pages(sample_pdf, tmp_path):
    """Only selected pages should be rotated."""
    output = tmp_path / "selected.pdf"

    rotate_pdf(
        sample_pdf,
        output,
        angle=180,
        pages=[1, 3],
    )

    reader = PdfReader(output)

    assert reader.pages[0].rotation == 180
    assert reader.pages[1].rotation == 0
    assert reader.pages[2].rotation == 180


def test_output_directory_created(sample_pdf, tmp_path):
    """Output directories should be created automatically."""
    output = tmp_path / "nested" / "folder" / "rotated.pdf"

    rotate_pdf(sample_pdf, output, angle=90)

    assert output.exists()


def test_metadata_preserved(tmp_path):
    """Metadata should be preserved after rotation."""
    pdf = tmp_path / "meta.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    writer.add_metadata(
        {
            "/Author": "Ultimate PDF",
            "/Title": "Rotation Test",
        }
    )

    with pdf.open("wb") as f:
        writer.write(f)

    output = tmp_path / "rotated.pdf"

    rotate_pdf(pdf, output, angle=90)

    reader = PdfReader(output)

    assert reader.metadata["/Author"] == "Ultimate PDF"
    assert reader.metadata["/Title"] == "Rotation Test"


def test_missing_pdf(tmp_path):
    """Missing input PDF should raise PDFNotFoundError."""
    with pytest.raises(PDFNotFoundError):
        rotate_pdf(
            tmp_path / "missing.pdf",
            tmp_path / "out.pdf",
            angle=90,
        )


def test_invalid_extension(tmp_path):
    """Non-PDF files should raise InvalidPDFError."""
    bad_file = tmp_path / "file.txt"
    bad_file.write_text("hello")

    with pytest.raises(InvalidPDFError):
        rotate_pdf(
            bad_file,
            tmp_path / "out.pdf",
            angle=90,
        )


def test_corrupted_pdf(tmp_path):
    """Corrupted PDFs should raise InvalidPDFError."""
    bad_pdf = tmp_path / "bad.pdf"
    bad_pdf.write_text("not a pdf")

    with pytest.raises(InvalidPDFError):
        rotate_pdf(
            bad_pdf,
            tmp_path / "out.pdf",
            angle=90,
        )


def test_invalid_page_number(sample_pdf, tmp_path):
    """Invalid page numbers should raise PageRangeError."""
    with pytest.raises(PageRangeError):
        rotate_pdf(
            sample_pdf,
            tmp_path / "out.pdf",
            angle=90,
            pages=[5],
        )


def test_empty_page_list(sample_pdf, tmp_path):
    """Empty page selection should raise PageRangeError."""
    with pytest.raises(PageRangeError):
        rotate_pdf(
            sample_pdf,
            tmp_path / "out.pdf",
            angle=90,
            pages=[],
        )


def test_invalid_angle(sample_pdf, tmp_path):
    """Invalid rotation angle should raise PDFOperationError."""
    with pytest.raises(PDFOperationError):
        rotate_pdf(
            sample_pdf,
            tmp_path / "out.pdf",
            angle=45,
        )


def test_overwrite_existing_output(sample_pdf, tmp_path):
    """Existing output files should be overwritten."""
    output = tmp_path / "rotated.pdf"

    output.write_text("old content")

    rotate_pdf(sample_pdf, output, angle=270)

    reader = PdfReader(output)

    assert len(reader.pages) == 3

    for page in reader.pages:
        assert page.rotation == 270