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
        EmptyInputError: If no input files are provided.
        PDFNotFoundError: If an input file does not exist.
        InvalidPDFError: If an input file is not a valid PDF.
        OutputFileError: If the output file cannot be created.
        PDFOperationError: If the merge operation fails.
    """

    # Validate all input files
    validate_pdf_list(input_files)

    writer = PdfWriter()

    try:
        # Append all input PDFs
        for pdf in input_files:
            writer.append(str(pdf))

        # Ensure the output directory exists
        output.parent.mkdir(parents=True, exist_ok=True)

        # Write the merged PDF
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