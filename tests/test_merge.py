from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from ultimate_pdf.core.exceptions import (
    EmptyInputError,
    InvalidPDFError,
    PDFNotFoundError,
)
from ultimate_pdf.core.merger import merge_pdfs


def create_pdf(path: Path, pages: int = 1) -> None:
    """
    Create a simple PDF with blank pages.
    """
    writer = PdfWriter()

    for _ in range(pages):
        writer.add_blank_page(width=595, height=842)

    with path.open("wb") as f:
        writer.write(f)


def test_merge_two_pdfs(tmp_path):
    """
    Merge two PDFs.
    """
    pdf1 = tmp_path / "first.pdf"
    pdf2 = tmp_path / "second.pdf"
    output = tmp_path / "merged.pdf"

    create_pdf(pdf1, pages=2)
    create_pdf(pdf2, pages=3)

    merge_pdfs([pdf1, pdf2], output)

    assert output.exists()

    reader = PdfReader(str(output))
    assert len(reader.pages) == 5


def test_merge_single_pdf(tmp_path):
    """
    Merge a single PDF.
    """
    pdf = tmp_path / "single.pdf"
    output = tmp_path / "merged.pdf"

    create_pdf(pdf, pages=4)

    merge_pdfs([pdf], output)

    assert output.exists()

    reader = PdfReader(str(output))
    assert len(reader.pages) == 4


def test_merge_multiple_pdfs(tmp_path):
    """
    Merge multiple PDFs.
    """
    pdf1 = tmp_path / "one.pdf"
    pdf2 = tmp_path / "two.pdf"
    pdf3 = tmp_path / "three.pdf"

    output = tmp_path / "merged.pdf"

    create_pdf(pdf1, pages=1)
    create_pdf(pdf2, pages=2)
    create_pdf(pdf3, pages=3)

    merge_pdfs(
        [pdf1, pdf2, pdf3],
        output,
    )

    reader = PdfReader(str(output))

    assert len(reader.pages) == 6


def test_merge_empty_input():
    """
    Empty input should fail.
    """
    with pytest.raises(EmptyInputError):
        merge_pdfs([], Path("merged.pdf"))


def test_merge_missing_pdf(tmp_path):
    """
    Missing PDF should fail.
    """
    missing = tmp_path / "missing.pdf"
    output = tmp_path / "merged.pdf"

    with pytest.raises(PDFNotFoundError):
        merge_pdfs([missing], output)


def test_merge_invalid_extension(tmp_path):
    """
    Non-PDF files should fail validation.
    """
    text_file = tmp_path / "notes.txt"
    text_file.write_text("Hello")

    output = tmp_path / "merged.pdf"

    with pytest.raises(InvalidPDFError):
        merge_pdfs([text_file], output)


def test_merge_invalid_pdf(tmp_path):
    """
    Corrupted PDF should fail validation.
    """
    fake_pdf = tmp_path / "fake.pdf"
    fake_pdf.write_text("This is not a PDF.")

    output = tmp_path / "merged.pdf"

    with pytest.raises(InvalidPDFError):
        merge_pdfs([fake_pdf], output)


def test_merge_creates_output_directory(tmp_path):
    """
    Output directory should be created automatically.
    """
    pdf1 = tmp_path / "input.pdf"
    create_pdf(pdf1)

    output = tmp_path / "nested" / "folder" / "merged.pdf"

    merge_pdfs([pdf1], output)

    assert output.exists()


def test_merge_overwrites_existing_output(tmp_path):
    """
    Existing output file should be overwritten.
    """
    pdf1 = tmp_path / "input.pdf"
    create_pdf(pdf1, pages=2)

    output = tmp_path / "merged.pdf"

    output.write_text("Old content")

    merge_pdfs([pdf1], output)

    reader = PdfReader(str(output))

    assert len(reader.pages) == 2