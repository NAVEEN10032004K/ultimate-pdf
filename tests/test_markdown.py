from pathlib import Path

import fitz
import pytest

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PageRangeError,
    PDFNotFoundError,
)
from ultimate_pdf.core.markdown_exporter import export_markdown


@pytest.fixture
def text_pdf(tmp_path):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello Markdown Export", fontsize=20)
    pdf = tmp_path / "doc.pdf"
    doc.save(pdf)
    doc.close()
    return pdf


def test_export_default_path(text_pdf):
    out = export_markdown(text_pdf)
    assert out == text_pdf.with_suffix(".md")
    assert "Hello Markdown Export" in out.read_text()


def test_export_custom_path(text_pdf, tmp_path):
    out = tmp_path / "nested" / "result.md"
    written = export_markdown(text_pdf, output_file=out)
    assert written == out
    assert out.exists()
    assert "Hello Markdown Export" in out.read_text()


def test_export_page_subset(text_pdf):
    out = export_markdown(text_pdf, pages="1")
    assert "Hello Markdown Export" in out.read_text()


def test_invalid_page(text_pdf):
    with pytest.raises(PageRangeError):
        export_markdown(text_pdf, pages="9")


def test_missing_pdf(tmp_path):
    with pytest.raises(PDFNotFoundError):
        export_markdown(tmp_path / "missing.pdf")


def test_invalid_extension(tmp_path):
    bad = tmp_path / "file.txt"
    bad.write_text("hello")
    with pytest.raises(InvalidPDFError):
        export_markdown(bad)
