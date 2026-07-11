from pathlib import Path

import fitz
import pytest
from pypdf import PdfReader

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PDFNotFoundError,
    PDFOperationError,
    UnsupportedFormatError,
)
from ultimate_pdf.core.watermarker import add_image_watermark, add_text_watermark


@pytest.fixture
def sample_pdf(tmp_path):
    doc = fitz.open()
    for _ in range(2):
        doc.new_page(width=300, height=300)
    pdf = tmp_path / "sample.pdf"
    doc.save(pdf)
    doc.close()
    return pdf


def make_png(path: Path) -> Path:
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 20, 20))
    pix.clear_with(200)
    pix.save(str(path))
    return path


def test_text_watermark(sample_pdf, tmp_path):
    out = tmp_path / "wm.pdf"
    add_text_watermark(sample_pdf, out, text="CONFIDENTIAL")
    assert len(PdfReader(str(out)).pages) == 2


def test_image_watermark(sample_pdf, tmp_path):
    img = make_png(tmp_path / "logo.png")
    out = tmp_path / "wm.pdf"
    add_image_watermark(sample_pdf, out, image=img)
    assert len(PdfReader(str(out)).pages) == 2


def test_text_watermark_page_subset(sample_pdf, tmp_path):
    out = tmp_path / "wm.pdf"
    add_text_watermark(sample_pdf, out, text="DRAFT", pages="1")
    assert len(PdfReader(str(out)).pages) == 2


def test_invalid_opacity(sample_pdf, tmp_path):
    with pytest.raises(PDFOperationError):
        add_text_watermark(sample_pdf, tmp_path / "wm.pdf", text="X", opacity=2.0)


def test_invalid_rotation(sample_pdf, tmp_path):
    with pytest.raises(PDFOperationError):
        add_text_watermark(sample_pdf, tmp_path / "wm.pdf", text="X", rotate=45)


def test_missing_pdf(tmp_path):
    with pytest.raises(PDFNotFoundError):
        add_text_watermark(tmp_path / "missing.pdf", tmp_path / "wm.pdf", text="X")


def test_invalid_extension(tmp_path):
    bad = tmp_path / "file.txt"
    bad.write_text("hello")
    with pytest.raises(InvalidPDFError):
        add_text_watermark(bad, tmp_path / "wm.pdf", text="X")


def test_bad_watermark_image(sample_pdf, tmp_path):
    bad = tmp_path / "logo.txt"
    bad.write_text("hello")
    with pytest.raises(UnsupportedFormatError):
        add_image_watermark(sample_pdf, tmp_path / "wm.pdf", image=bad)
