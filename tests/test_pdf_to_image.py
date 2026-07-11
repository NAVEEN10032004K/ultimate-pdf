from pathlib import Path

import pytest
from pypdf import PdfWriter

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PageRangeError,
    PDFNotFoundError,
)
from ultimate_pdf.core.rasterizer import pdf_to_images


@pytest.fixture
def sample_pdf(tmp_path):
    pdf = tmp_path / "sample.pdf"
    writer = PdfWriter()
    for _ in range(3):
        writer.add_blank_page(width=300, height=300)
    with pdf.open("wb") as f:
        writer.write(f)
    return pdf


def test_convert_all_pages(sample_pdf, tmp_path):
    out = tmp_path / "imgs"
    count = pdf_to_images(sample_pdf, output_dir=out, dpi=72)
    assert count == 3
    assert len(list(out.glob("*.png"))) == 3


def test_default_output_dir(sample_pdf):
    count = pdf_to_images(sample_pdf, dpi=72)
    out = sample_pdf.parent / "sample_images"
    assert count == 3
    assert out.exists()


def test_custom_format(sample_pdf, tmp_path):
    out = tmp_path / "imgs"
    pdf_to_images(sample_pdf, output_dir=out, dpi=72, fmt="jpg")
    assert len(list(out.glob("*.jpg"))) == 3


def test_page_subset(sample_pdf, tmp_path):
    out = tmp_path / "imgs"
    count = pdf_to_images(sample_pdf, output_dir=out, dpi=72, pages="1,3")
    assert count == 2
    assert len(list(out.glob("*.png"))) == 2


def test_invalid_page(sample_pdf, tmp_path):
    with pytest.raises(PageRangeError):
        pdf_to_images(sample_pdf, output_dir=tmp_path / "imgs", pages="9")


def test_missing_pdf(tmp_path):
    with pytest.raises(PDFNotFoundError):
        pdf_to_images(tmp_path / "missing.pdf")


def test_invalid_extension(tmp_path):
    bad = tmp_path / "file.txt"
    bad.write_text("hello")
    with pytest.raises(InvalidPDFError):
        pdf_to_images(bad)
