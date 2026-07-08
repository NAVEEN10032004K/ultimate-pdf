from pathlib import Path

import fitz

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
)
from ultimate_pdf.core.validator import validate_pdf


def compress_pdf(
    input_path: Path,
    output_path: Path,
) -> None:
    """
    Compress a PDF by optimizing its internal structure while preserving
    text, images, fonts, links, and vector graphics.
    """

    validate_pdf(input_path)

    document = None

    try:
        document = fitz.open(input_path)

        document.save(
            output_path,
            garbage=4,
            clean=True,
            deflate=True,
            deflate_images=True,
            deflate_fonts=True,
            use_objstms=1,
        )

    except RuntimeError as exc:
        raise OutputFileError(
            f"Failed to save compressed PDF: {exc}"
        ) from exc

    except Exception as exc:
        raise PDFOperationError(
            f"Failed to compress PDF: {exc}"
        ) from exc

    finally:
        if document is not None:
            document.close()