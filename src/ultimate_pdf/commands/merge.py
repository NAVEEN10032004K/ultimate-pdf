from pathlib import Path

import typer

from ultimate_pdf.core.exceptions import (
    EmptyInputError,
    InvalidPDFError,
    OutputFileError,
    PDFNotFoundError,
    PDFOperationError,
)
from ultimate_pdf.core.merger import merge_pdfs


def merge(
    input_files: list[Path] = typer.Argument(
        ...,
        metavar="INPUT_FILES",
        help="PDF files to merge.",
    ),
    output: Path = typer.Option(
        Path("merged.pdf"),
        "--output",
        "-o",
        metavar="OUTPUT",
        help="Output PDF file.",
    ),
):
    """
    Merge multiple PDF files into a single PDF.
    """

    try:
        merge_pdfs(input_files, output)

        typer.secho(
            f"✅ Successfully merged {len(input_files)} PDF(s) into '{output}'.",
            fg=typer.colors.GREEN,
        )

    except (
        EmptyInputError,
        PDFNotFoundError,
        InvalidPDFError,
        OutputFileError,
        PDFOperationError,
    ) as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)