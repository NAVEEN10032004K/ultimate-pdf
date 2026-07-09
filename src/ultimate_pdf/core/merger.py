from pathlib import Path

from pypdf import PdfWriter

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
)
from ultimate_pdf.core.validator import validate_pdf_list


def merge_pdfs(input_files: list[Path], output: Path) -> None:
    """
    Merge multiple PDF files into a single PDF.

    Args:
        input_files: List of input PDF files.
        output: Output PDF file path.

    Raises:
        OutputFileError: If the output file cannot be created.
        PDFOperationError: If the merge operation fails.
    """

    validate_pdf_list(input_files)

    writer = PdfWriter()

    try:
        for pdf in input_files:
            writer.append(str(pdf))

        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("wb") as merged_pdf:
            writer.write(merged_pdf)

    except OSError as e:
        raise OutputFileError(
            f"Unable to create output file: {output}"
        ) from e

    except Exception as e:
        raise PDFOperationError(
            f"Failed to merge PDF files: {e}"
        ) from e

    finally:
        writer.close()