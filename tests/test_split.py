from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from ultimate_pdf.core.exceptions import (
    InvalidPDFError,
    PageRangeError,
    PDFNotFoundError,
)
from ultimate_pdf.core.splitter import (
    split_every_n_pages,
    split_page_range,
    split_selected_pages,
    split_to_pages,
)


def create_pdf(path: Path, pages: int = 1) -> None:
    """
    Create a simple PDF with blank pages.
    """
    writer = PdfWriter()

    for _ in range(pages):
        writer.add_blank_page(width=595, height=842)

    with path.open("wb") as f:
        writer.write(f)


def test_split_to_pages(tmp_path):
    pdf = tmp_path / "sample.pdf"
    create_pdf(pdf, pages=4)

    count = split_to_pages(pdf)

    output_dir = tmp_path / "sample_pages"

    assert count == 4
    assert output_dir.exists()

    files = sorted(output_dir.glob("*.pdf"))

    assert len(files) == 4

    for file in files:
        reader = PdfReader(str(file))
        assert len(reader.pages) == 1


def test_split_page_range(tmp_path):
    pdf = tmp_path / "sample.pdf"
    output = tmp_path / "range.pdf"

    create_pdf(pdf, pages=6)

    split_page_range(pdf, 2, 4, output)

    reader = PdfReader(str(output))

    assert len(reader.pages) == 3


def test_split_every_n_pages(tmp_path):
    pdf = tmp_path / "sample.pdf"

    create_pdf(pdf, pages=7)

    count = split_every_n_pages(pdf, 3)

    output_dir = tmp_path / "sample_split"

    assert count == 3

    files = sorted(output_dir.glob("*.pdf"))

    assert len(files) == 3

    assert len(PdfReader(str(files[0])).pages) == 3
    assert len(PdfReader(str(files[1])).pages) == 3
    assert len(PdfReader(str(files[2])).pages) == 1


def test_split_selected_pages(tmp_path):
    pdf = tmp_path / "sample.pdf"
    output = tmp_path / "selected.pdf"

    create_pdf(pdf, pages=5)

    split_selected_pages(pdf, [1, 3, 5], output)

    reader = PdfReader(str(output))

    assert len(reader.pages) == 3


def test_split_invalid_page_range(tmp_path):
    pdf = tmp_path / "sample.pdf"

    create_pdf(pdf, pages=5)

    with pytest.raises(PageRangeError):
        split_page_range(
            pdf,
            5,
            2,
            tmp_path / "out.pdf",
        )


def test_split_page_out_of_range(tmp_path):
    pdf = tmp_path / "sample.pdf"

    create_pdf(pdf, pages=4)

    with pytest.raises(PageRangeError):
        split_page_range(
            pdf,
            1,
            10,
            tmp_path / "out.pdf",
        )


def test_split_every_invalid_number(tmp_path):
    pdf = tmp_path / "sample.pdf"

    create_pdf(pdf)

    with pytest.raises(PageRangeError):
        split_every_n_pages(pdf, 0)


def test_split_selected_invalid_page(tmp_path):
    pdf = tmp_path / "sample.pdf"

    create_pdf(pdf, pages=3)

    with pytest.raises(PageRangeError):
        split_selected_pages(
            pdf,
            [1, 5],
            tmp_path / "out.pdf",
        )


def test_split_selected_empty(tmp_path):
    pdf = tmp_path / "sample.pdf"

    create_pdf(pdf, pages=3)

    with pytest.raises(PageRangeError):
        split_selected_pages(
            pdf,
            [],
            tmp_path / "out.pdf",
        )


def test_split_missing_pdf(tmp_path):
    with pytest.raises(PDFNotFoundError):
        split_to_pages(tmp_path / "missing.pdf")


def test_split_invalid_extension(tmp_path):
    file = tmp_path / "notes.txt"
    file.write_text("Hello")

    with pytest.raises(InvalidPDFError):
        split_to_pages(file)


def test_split_invalid_pdf(tmp_path):
    fake = tmp_path / "fake.pdf"
    fake.write_text("Not a PDF")

    with pytest.raises(InvalidPDFError):
        split_to_pages(fake)