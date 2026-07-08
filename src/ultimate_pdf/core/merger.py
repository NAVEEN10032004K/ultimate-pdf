from pathlib import Path

from pypdf import PdfWriter

from ultimate_pdf.core.validator import validate_pdf_list


def merge_pdfs(input_files: list[Path], output: Path) -> None:
    """
    Merge multiple PDF files into a single PDF.

    Args:
        input_files: List of input PDF files.
        output: Output PDF file path.

    Raises:
        FileNotFoundError: If any input file does not exist.
        ValueError: If the input list is empty or contains invalid files.
        Exception: Any error raised by pypdf while merging.
    """

    # Validate all input files
    validate_pdf_list(input_files)

    writer = PdfWriter()

    try:
        for pdf in input_files:
            writer.append(str(pdf))

        # Ensure the output directory exists
        output.parent.mkdir(parents=True, exist_ok=True)

        # Write the merged PDF
        with open(output, "wb") as merged_pdf:
            writer.write(merged_pdf)

    finally:
        writer.close()