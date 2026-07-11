from pathlib import Path

from pypdf import PdfWriter

from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
    PDFPasswordError,
    UltimatePDFError,
)
from ultimate_pdf.core.parser import get_metadata, get_reader


def encrypt_pdf(
    input_file: Path,
    output_file: Path,
    password: str,
) -> None:
    """
    Encrypt a PDF with the given password.
    """
    if not password.strip():
        raise PDFPasswordError("Password cannot be empty.")

    try:
        reader = get_reader(input_file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        metadata = get_metadata(input_file)
        if metadata:
            writer.add_metadata(metadata)

        writer.encrypt(password)

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
            f"Failed to encrypt PDF: {e}"
        ) from e


def decrypt_pdf(
    input_file: Path,
    output_file: Path,
    password: str,
) -> None:
    """
    Decrypt a password-protected PDF.
    """
    if not password.strip():
        raise PDFPasswordError("Password cannot be empty.")

    try:
        reader = get_reader(input_file)

        if not reader.is_encrypted:
            raise PDFPasswordError("PDF is not encrypted.")

        result = reader.decrypt(password)

        if result == 0:
            raise PDFPasswordError("Incorrect password.")

        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        metadata = reader.metadata or {}
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
            f"Failed to decrypt PDF: {e}"
        ) from e