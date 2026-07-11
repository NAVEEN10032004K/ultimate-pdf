from pathlib import Path

from pypdf import PdfWriter

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PageRangeError,
    PDFOperationError,
    UltimatePDFError,
)
from ultimate_pdf.core.parser import get_metadata, get_reader


def rotate_pdf(
    input_file: Path,
    output_file: Path,
    angle: int,
    pages: list[int] | None = None,
) -> None:
    """
    Rotate pages in a PDF.

    Args:
        input_file: Input PDF.
        output_file: Output PDF.
        angle: Rotation angle (90, 180, or 270).
        pages: Pages to rotate (1-based). If None, rotate all pages.

    Raises:
        PageRangeError: If a page number is invalid.
        OutputFileError: If the output file cannot be written.
        PDFOperationError: If the rotation operation fails.
    """

    if angle not in (90, 180, 270):
        raise PDFOperationError(
            "Rotation angle must be one of: 90, 180, or 270."
        )

    try:
        reader = get_reader(input_file)
        writer = PdfWriter()

        total_pages = len(reader.pages)

        if pages is None:
            pages_to_rotate = set(range(1, total_pages + 1))
        else:
            if not pages:
                raise PageRangeError(
                    "At least one page must be specified."
                )

            pages_to_rotate = set()

            for page in pages:
                if page < 1 or page > total_pages:
                    raise PageRangeError(
                        f"Page {page} is out of range. "
                        f"PDF contains {total_pages} pages."
                    )

                pages_to_rotate.add(page)

        for index, page in enumerate(reader.pages, start=1):
            if index in pages_to_rotate:
                page.rotate(angle)

            writer.add_page(page)

        metadata = get_metadata(input_file)
        if metadata:
            writer.add_metadata(metadata)

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("wb") as f:
            writer.write(f)

    except UltimatePDFError:
        raise

    except OSError as e:
        raise OutputFileError(
            f"Unable to write output file '{output_file}'."
        ) from e

    except Exception as e:
        raise PDFOperationError(
            f"Failed to rotate PDF: {e}"
        ) from e