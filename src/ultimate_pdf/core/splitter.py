from pathlib import Path

from pypdf import PdfReader, PdfWriter

from ultimate_pdf.core.validator import validate_pdf


def split_to_pages(input_file: Path) -> int:
    """
    Split a PDF into individual pages.

    Args:
        input_file: Path to the input PDF.

    Returns:
        Number of PDF files created.
    """

    validate_pdf(input_file)

    reader = PdfReader(str(input_file))

    output_dir = input_file.parent / input_file.stem
    output_dir.mkdir(exist_ok=True)

    for page_number, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)

        output_file = output_dir / f"{input_file.stem}_page_{page_number}.pdf"

        with output_file.open("wb") as pdf:
            writer.write(pdf)

        writer.close()

    return len(reader.pages)


def split_page_range(
    input_file: Path,
    start_page: int,
    end_page: int,
    output_file: Path,
) -> None:
    """
    Extract a page range from a PDF into a new PDF.

    Args:
        input_file: Source PDF.
        start_page: First page (1-based).
        end_page: Last page (1-based).
        output_file: Output PDF.

    Raises:
        ValueError: If the page range is invalid.
    """

    validate_pdf(input_file)

    reader = PdfReader(str(input_file))
    total_pages = len(reader.pages)

    # Validate page numbers
    if start_page < 1:
        raise ValueError("Start page must be greater than 0.")

    if end_page > total_pages:
        raise ValueError(f"End page ({end_page}) exceeds total pages ({total_pages}).")

    if start_page > end_page:
        raise ValueError("Start page cannot be greater than end page.")

    writer = PdfWriter()

    try:
        # Convert to zero-based indexing
        for page_number in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_number])

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("wb") as pdf:
            writer.write(pdf)

    finally:
        writer.close()


def split_every_n_pages(
    input_file: Path,
    pages_per_file: int,
) -> int:
    """
    Split a PDF into multiple PDFs with a fixed number of pages.

    Returns:
        Number of PDF files created.
    """

    validate_pdf(input_file)

    if pages_per_file <= 0:
        raise ValueError("Pages per file must be greater than 0.")

    reader = PdfReader(str(input_file))
    total_pages = len(reader.pages)

    output_dir = input_file.parent / input_file.stem
    output_dir.mkdir(exist_ok=True)

    file_count = 0

    for start in range(0, total_pages, pages_per_file):
        writer = PdfWriter()

        end = min(start + pages_per_file, total_pages)

        for page in range(start, end):
            writer.add_page(reader.pages[page])

        output_file = output_dir / f"{input_file.stem}_part_{file_count + 1}.pdf"

        with output_file.open("wb") as pdf:
            writer.write(pdf)

        writer.close()
        file_count += 1

    return file_count


def split_selected_pages(
    input_file: Path,
    pages: list[int],
    output_file: Path,
) -> None:
    """
    Extract selected pages into a new PDF.
    """

    validate_pdf(input_file)

    reader = PdfReader(str(input_file))
    total_pages = len(reader.pages)

    writer = PdfWriter()

    for page in pages:

        if page < 1 or page > total_pages:
            raise ValueError(
                f"Page {page} is out of range. PDF has {total_pages} pages."
            )

        writer.add_page(reader.pages[page - 1])

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("wb") as pdf:
        writer.write(pdf)

    writer.close()
