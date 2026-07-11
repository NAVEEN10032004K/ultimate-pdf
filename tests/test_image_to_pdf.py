from pathlib import Path

import fitz
import pytest
from pypdf import PdfReader

from ultimate_pdf.core.exceptions import (
    EmptyInputError,
    PDFNotFoundError,
    UnsupportedFormatError,
)
from ultimate_pdf.core.image_converter import images_to_pdf


def make_png(path: Path) -> Path:
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 20, 20))
    pix.clear_with(200)
    pix.save(str(path))
    return path


def test_single_image(tmp_path):
    img = make_png(tmp_path / "a.png")
    out = tmp_path / "out.pdf"
    images_to_pdf([img], out)
    assert len(PdfReader(str(out)).pages) == 1


def test_multiple_images(tmp_path):
    imgs = [make_png(tmp_path / f"{n}.png") for n in range(3)]
    out = tmp_path / "out.pdf"
    images_to_pdf(imgs, out)
    assert len(PdfReader(str(out)).pages) == 3


def test_output_dir_created(tmp_path):
    img = make_png(tmp_path / "a.png")
    out = tmp_path / "nested" / "out.pdf"
    images_to_pdf([img], out)
    assert out.exists()


def test_empty_list(tmp_path):
    with pytest.raises(EmptyInputError):
        images_to_pdf([], tmp_path / "out.pdf")


def test_non_image(tmp_path):
    bad = tmp_path / "file.txt"
    bad.write_text("hello")
    with pytest.raises(UnsupportedFormatError):
        images_to_pdf([bad], tmp_path / "out.pdf")


def test_missing_image(tmp_path):
    with pytest.raises(PDFNotFoundError):
        images_to_pdf([tmp_path / "missing.png"], tmp_path / "out.pdf")
