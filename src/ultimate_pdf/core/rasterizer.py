from pathlib import Path

import fitz

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
    UltimatePDFError,
)
from ultimate_pdf.core.parser import parse_page_list
from ultimate_pdf.core.validator import validate_pdf


def pdf_to_images(
    input_file: Path,
    output_dir: Path | None = None,
    dpi: int = 200,
    fmt: str = "png",
    pages: str | None = None,
) -> int:
    """
    Render PDF pages to image files.

    Args:
        input_file: Input PDF.
        output_dir: Directory for the images. Defaults to '<stem>_images' beside the PDF.
        dpi: Render resolution.
        fmt: Image format/extension (png, jpg, ...).
        pages: Optional page selection like '1,3,5' or '2-4' (1-based). All pages if None.

    Returns:
        Number of images written.

    Raises:
        PageRangeError, OutputFileError, PDFOperationError.
    """

    validate_pdf(input_file)

    if output_dir is None:
        output_dir = input_file.parent / f"{input_file.stem}_images"

    document = None

    try:
        document = fitz.open(input_file)
        total_pages = document.page_count

        if pages is None:
            page_numbers = list(range(1, total_pages + 1))
        else:
            page_numbers = parse_page_list(pages, total_pages)

        output_dir.mkdir(parents=True, exist_ok=True)

        for number in page_numbers:
            page = document[number - 1]
            pixmap = page.get_pixmap(dpi=dpi)
            pixmap.save(output_dir / f"{input_file.stem}_page_{number}.{fmt}")

        return len(page_numbers)

    except UltimatePDFError:
        raise

    except OSError as exc:
        raise OutputFileError(
            f"Unable to write images to '{output_dir}'."
        ) from exc

    except Exception as exc:
        raise PDFOperationError(f"Failed to convert PDF to images: {exc}") from exc

    finally:
        if document is not None:
            document.close()
