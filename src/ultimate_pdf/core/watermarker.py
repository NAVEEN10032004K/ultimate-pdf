from pathlib import Path

import fitz

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
    UltimatePDFError,
)
from ultimate_pdf.core.parser import parse_page_list
from ultimate_pdf.core.validator import validate_image, validate_pdf

# ponytail: insert_textbox rotate only accepts 0/90/180/270; a true 45° diagonal
# needs a Shape + morph matrix. Start orthogonal; add morph only if a diagonal is required.
_ALLOWED_ROTATIONS = (0, 90, 180, 270)


def _select_pages(document: fitz.Document, pages: str | None) -> list[int]:
    if pages is None:
        return list(range(1, document.page_count + 1))
    return parse_page_list(pages, document.page_count)


def add_text_watermark(
    input_file: Path,
    output_file: Path,
    text: str,
    opacity: float = 0.15,
    size: int = 48,
    color: tuple[float, float, float] = (0.5, 0.5, 0.5),
    rotate: int = 0,
    pages: str | None = None,
) -> None:
    """
    Stamp a centered text watermark onto the selected pages.

    Raises:
        PageRangeError, OutputFileError, PDFOperationError.
    """

    validate_pdf(input_file)

    if rotate not in _ALLOWED_ROTATIONS:
        raise PDFOperationError(
            f"Rotation must be one of {_ALLOWED_ROTATIONS}."
        )

    if not 0.0 <= opacity <= 1.0:
        raise PDFOperationError("Opacity must be between 0.0 and 1.0.")

    document = None
    try:
        document = fitz.open(input_file)

        for number in _select_pages(document, pages):
            page = document[number - 1]
            rect = page.rect
            box = fitz.Rect(0, rect.height / 2 - size, rect.width, rect.height / 2 + size)
            page.insert_textbox(
                box,
                text,
                fontsize=size,
                color=color,
                fill_opacity=opacity,
                rotate=rotate,
                align=fitz.TEXT_ALIGN_CENTER,
            )

        _save(document, output_file)

    except UltimatePDFError:
        raise
    except OSError as exc:
        raise OutputFileError(f"Unable to write output file '{output_file}'.") from exc
    except Exception as exc:
        raise PDFOperationError(f"Failed to add text watermark: {exc}") from exc
    finally:
        if document is not None:
            document.close()


def add_image_watermark(
    input_file: Path,
    output_file: Path,
    image: Path,
    opacity: float = 0.15,
    pages: str | None = None,
) -> None:
    """
    Stamp an image watermark (scaled to the page) onto the selected pages.

    Raises:
        PageRangeError, UnsupportedFormatError, OutputFileError, PDFOperationError.
    """

    validate_pdf(input_file)
    validate_image(image)

    if not 0.0 <= opacity <= 1.0:
        raise PDFOperationError("Opacity must be between 0.0 and 1.0.")

    document = None
    try:
        pixmap = fitz.Pixmap(str(image))
        if not pixmap.alpha:
            pixmap = fitz.Pixmap(pixmap, 1)  # add an alpha channel
        # uniform per-pixel opacity
        pixmap.set_alpha(bytes([int(opacity * 255)]) * (pixmap.width * pixmap.height))

        document = fitz.open(input_file)

        for number in _select_pages(document, pages):
            page = document[number - 1]
            page.insert_image(page.rect, pixmap=pixmap, overlay=True)

        _save(document, output_file)

    except UltimatePDFError:
        raise
    except OSError as exc:
        raise OutputFileError(f"Unable to write output file '{output_file}'.") from exc
    except Exception as exc:
        raise PDFOperationError(f"Failed to add image watermark: {exc}") from exc
    finally:
        if document is not None:
            document.close()


def _save(document: fitz.Document, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_file)
