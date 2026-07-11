import shutil
from pathlib import Path

import fitz

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
    UltimatePDFError,
)
from ultimate_pdf.core.parser import parse_page_list
from ultimate_pdf.core.validator import validate_pdf

_TESSERACT_HINT = (
    "OCR requires the Tesseract engine. Install it with "
    "'brew install tesseract' (macOS) or 'apt install tesseract-ocr' (Linux). "
    "If tessdata is not found, set the TESSDATA_PREFIX environment variable."
)


def ocr_pdf(
    input_file: Path,
    output_file: Path | None = None,
    mode: str = "pdf",
    language: str = "eng",
    dpi: int = 300,
    pages: str | None = None,
) -> str | None:
    """
    Run OCR on a PDF.

    mode='pdf':  produce a searchable PDF (invisible text layer). Requires output_file.
    mode='text': return the recognized text; also written to output_file if given.

    Raises:
        PageRangeError, OutputFileError, PDFOperationError (incl. missing Tesseract).
    """

    validate_pdf(input_file)

    if mode not in ("pdf", "text"):
        raise PDFOperationError("Mode must be 'pdf' or 'text'.")

    if mode == "pdf" and output_file is None:
        raise PDFOperationError("An output file is required for 'pdf' mode.")

    if shutil.which("tesseract") is None:
        raise PDFOperationError(_TESSERACT_HINT)

    document = None
    out = None
    try:
        document = fitz.open(input_file)

        if pages is None:
            page_numbers = list(range(1, document.page_count + 1))
        else:
            page_numbers = parse_page_list(pages, document.page_count)

        if mode == "pdf":
            out = fitz.open()
            for number in page_numbers:
                pixmap = document[number - 1].get_pixmap(dpi=dpi)
                pdf_bytes = pixmap.pdfocr_tobytes(language=language)
                with fitz.open("pdf", pdf_bytes) as page_pdf:
                    out.insert_pdf(page_pdf)

            output_file.parent.mkdir(parents=True, exist_ok=True)
            out.save(output_file)
            return None

        # text mode
        chunks: list[str] = []
        for number in page_numbers:
            page = document[number - 1]
            textpage = page.get_textpage_ocr(language=language, dpi=dpi, full=True)
            chunks.append(page.get_text(textpage=textpage))
        text = "\n".join(chunks)

        if output_file is not None:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(text, encoding="utf-8")

        return text

    except UltimatePDFError:
        raise
    except OSError as exc:
        raise OutputFileError(f"Unable to write output file '{output_file}'.") from exc
    except Exception as exc:
        # PyMuPDF raises RuntimeError when Tesseract/tessdata is unavailable.
        raise PDFOperationError(f"OCR failed: {exc}. {_TESSERACT_HINT}") from exc
    finally:
        if out is not None:
            out.close()
        if document is not None:
            document.close()
