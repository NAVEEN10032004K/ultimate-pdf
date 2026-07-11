import shutil
from pathlib import Path

import fitz
import pytest
from pypdf import PdfReader

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PDFNotFoundError,
    PDFOperationError,
)
from ultimate_pdf.core.ocr import ocr_pdf

tesseract = pytest.mark.skipif(
    shutil.which("tesseract") is None,
    reason="Tesseract binary not installed",
)


@pytest.fixture
def scanned_pdf(tmp_path):
    """A PDF whose page is a rasterized image of the text (no real text layer)."""
    doc = fitz.open()
    page = doc.new_page(width=400, height=200)
    page.insert_text((40, 100), "HELLO OCR", fontsize=40)
    pix = page.get_pixmap(dpi=200)

    scanned = fitz.open()
    img_page = scanned.new_page(width=page.rect.width, height=page.rect.height)
    img_page.insert_image(img_page.rect, pixmap=pix)
    out = tmp_path / "scan.pdf"
    scanned.save(out)
    scanned.close()
    doc.close()
    return out


@tesseract
def test_ocr_text_mode(scanned_pdf):
    text = ocr_pdf(scanned_pdf, mode="text")
    assert "HELLO" in text.upper()


@tesseract
def test_ocr_pdf_mode(scanned_pdf, tmp_path):
    out = tmp_path / "searchable.pdf"
    ocr_pdf(scanned_pdf, output_file=out, mode="pdf")
    reader = PdfReader(str(out))
    assert len(reader.pages) == 1
    assert "HELLO" in reader.pages[0].extract_text().upper()


def test_pdf_mode_requires_output(scanned_pdf):
    with pytest.raises(PDFOperationError):
        ocr_pdf(scanned_pdf, mode="pdf")


def test_invalid_mode(scanned_pdf, tmp_path):
    with pytest.raises(PDFOperationError):
        ocr_pdf(scanned_pdf, output_file=tmp_path / "o.pdf", mode="bogus")


def test_missing_pdf(tmp_path):
    with pytest.raises(PDFNotFoundError):
        ocr_pdf(tmp_path / "missing.pdf", output_file=tmp_path / "o.pdf")


def test_invalid_extension(tmp_path):
    bad = tmp_path / "file.txt"
    bad.write_text("hello")
    with pytest.raises(InvalidPDFError):
        ocr_pdf(bad, output_file=tmp_path / "o.pdf")
