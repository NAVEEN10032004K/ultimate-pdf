from pathlib import Path

import fitz

from ultimate_pdf.core.exceptions import (
    EmptyInputError,
    OutputFileError,
    PDFOperationError,
    UltimatePDFError,
)
from ultimate_pdf.core.validator import validate_image


def images_to_pdf(input_files: list[Path], output: Path) -> None:
    """
    Combine one or more images into a single PDF (one image per page).

    Raises:
        EmptyInputError, UnsupportedFormatError, PDFNotFoundError,
        OutputFileError, PDFOperationError.
    """

    if not input_files:
        raise EmptyInputError("At least one image file is required.")

    for image in input_files:
        validate_image(image)

    out = fitz.open()

    try:
        for image in input_files:
            with fitz.open(str(image)) as img:
                pdf_bytes = img.convert_to_pdf()
            with fitz.open("pdf", pdf_bytes) as page_pdf:
                out.insert_pdf(page_pdf)

        output.parent.mkdir(parents=True, exist_ok=True)
        out.save(output)

    except UltimatePDFError:
        raise

    except OSError as exc:
        raise OutputFileError(
            f"Unable to write output file '{output}'."
        ) from exc

    except Exception as exc:
        raise PDFOperationError(f"Failed to convert images to PDF: {exc}") from exc

    finally:
        out.close()
