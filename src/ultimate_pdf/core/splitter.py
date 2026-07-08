from pathlib import Path

from pypdf import PdfReader, PdfWriter

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
    PageRangeError,
)
from ultimate_pdf.core.validator import validate_pdf


def split_to_pages(input_file: Path) -> int:
    """
    Split a PDF into individual pages.

    Returns:
        Number of PDF files created.
    """
    validate_pdf(input_file)

    output_dir = input_file.parent / f"{input_file.stem}_pages"

    try:
        reader = PdfReader(input_file)

        output_dir.mkdir(parents=True, exist_ok=True)

        for page_number, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)

            output_file = output_dir / f"page_{page_number}.pdf"

            with output_file.open("wb") as f:
                writer.write(f)

        return len(reader.pages)

    except OSError as e:
        raise OutputFileError(
            f"Unable to write output files to '{output_dir}'."
        ) from e

    except Exception as e:
        raise PDFOperationError(
            f"Failed to split PDF: {e}"
        ) from e


def split_page_range(
    input_file: Path,
    start_page: int,
    end_page: int,
    output_file: Path,
) -> None:
    """
    Extract a page range into a new PDF.
    """
    validate_pdf(input_file)

    try:
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)

        if start_page < 1 or end_page > total_pages or start_page > end_page:
            raise PageRangeError(
                f"Invalid page range: {start_page}-{end_page}. "
                f"PDF contains {total_pages} pages."
            )

        writer = PdfWriter()

        for page in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page])

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("wb") as f:
            writer.write(f)

    except PageRangeError:
        raise

    except OSError as e:
        raise OutputFileError(
            f"Unable to write output file '{output_file}'."
        ) from e

    except Exception as e:
        raise PDFOperationError(
            f"Failed to extract page range: {e}"
        ) from e


def split_every_n_pages(
    input_file: Path,
    pages_per_file: int,
) -> int:
    """
    Split a PDF into multiple PDFs containing N pages each.

    Returns:
        Number of PDF files created.
    """
    validate_pdf(input_file)

    if pages_per_file <= 0:
        raise PageRangeError(
            "Pages per file must be greater than zero."
        )

    output_dir = input_file.parent / f"{input_file.stem}_split"

    try:
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)

        output_dir.mkdir(parents=True, exist_ok=True)

        file_number = 1

        for start in range(0, total_pages, pages_per_file):
            writer = PdfWriter()

            for page in range(start, min(start + pages_per_file, total_pages)):
                writer.add_page(reader.pages[page])

            output_file = output_dir / f"part_{file_number}.pdf"

            with output_file.open("wb") as f:
                writer.write(f)

            file_number += 1

        return file_number - 1

    except OSError as e:
        raise OutputFileError(
            f"Unable to write output files to '{output_dir}'."
        ) from e

    except Exception as e:
        raise PDFOperationError(
            f"Failed to split PDF: {e}"
        ) from e


def split_selected_pages(
    input_file: Path,
    selected_pages: list[int],
    output_file: Path,
) -> None:
    """
    Extract selected pages into a new PDF.
    """
    validate_pdf(input_file)

    try:
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)

        if not selected_pages:
            raise PageRangeError(
                "At least one page must be selected."
            )

        writer = PdfWriter()

        for page in selected_pages:
            if page < 1 or page > total_pages:
                raise PageRangeError(
                    f"Page {page} is out of range. "
                    f"PDF contains {total_pages} pages."
                )

            writer.add_page(reader.pages[page - 1])

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("wb") as f:
            writer.write(f)

    except PageRangeError:
        raise

    except OSError as e:
        raise OutputFileError(
            f"Unable to write output file '{output_file}'."
        ) from e

    except Exception as e:
        raise PDFOperationError(
            f"Failed to extract selected pages: {e}"
        ) from e