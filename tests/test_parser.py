from pathlib import Path

import pytest

from ultimate_pdf.core.exceptions import (
    PageRangeError,
)

from ultimate_pdf.core.parser import (
    extract_all_text,
    extract_page_text,
    get_metadata,
    get_page_count,
    get_pdf_info,
)

PDF_FILE = Path("paper.pdf")


def test_get_page_count():
    assert get_page_count(PDF_FILE) == 12


def test_get_metadata():
    metadata = get_metadata(PDF_FILE)

    assert isinstance(metadata, dict)


def test_get_pdf_info():
    info = get_pdf_info(PDF_FILE)

    assert info.file_name == "paper.pdf"
    assert info.page_count == 12
    assert info.encrypted is False


def test_extract_page_text():
    text = extract_page_text(PDF_FILE, 0)

    assert isinstance(text, str)
    assert len(text) > 0


def test_extract_all_text():
    text = extract_all_text(PDF_FILE)

    assert isinstance(text, str)
    assert len(text) > 0


def test_invalid_page_number():
    with pytest.raises(PageRangeError):
        extract_page_text(PDF_FILE, 100)
