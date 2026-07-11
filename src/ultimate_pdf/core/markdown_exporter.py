from pathlib import Path

import fitz
import pymupdf4llm

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
    UltimatePDFError,
)
from ultimate_pdf.core.parser import parse_page_list
from ultimate_pdf.core.validator import validate_pdf


def export_markdown(
    input_file: Path,
    output_file: Path | None = None,
    pages: str | None = None,
) -> Path:
    """
    Export a PDF's text content to a Markdown file.

    Args:
        input_file: Input PDF.
        output_file: Output .md path. Defaults to '<stem>.md' beside the PDF.
        pages: Optional page selection like '1,3,5' or '2-4' (1-based). All pages if None.

    Returns:
        The path of the written Markdown file.

    Raises:
        PageRangeError, OutputFileError, PDFOperationError.
    """

    validate_pdf(input_file)

    if output_file is None:
        output_file = input_file.with_suffix(".md")

    try:
        page_indices = None
        if pages is not None:
            with fitz.open(input_file) as document:
                total = document.page_count
            # pymupdf4llm expects 0-based page numbers
            page_indices = [n - 1 for n in parse_page_list(pages, total)]

        markdown = pymupdf4llm.to_markdown(str(input_file), pages=page_indices)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(markdown, encoding="utf-8")

        return output_file

    except UltimatePDFError:
        raise
    except OSError as exc:
        raise OutputFileError(f"Unable to write output file '{output_file}'.") from exc
    except Exception as exc:
        raise PDFOperationError(f"Failed to export Markdown: {exc}") from exc
