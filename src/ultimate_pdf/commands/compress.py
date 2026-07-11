from pathlib import Path

import typer

from ultimate_pdf.core.compressor import compress_pdf
from ultimate_pdf.core.exceptions import (
    OutputFileError,
    PDFOperationError,
)


def compress(
    input_pdf: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Input PDF file.",
    ),
    output_pdf: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output PDF file. Defaults to '<input>_compressed.pdf'.",
    ),
) -> None:
    """
    Compress a PDF.
    """

    if output_pdf is None:
        output_pdf = input_pdf.with_name(
            f"{input_pdf.stem}_compressed.pdf"
        )

    try:
        compress_pdf(
            input_path=input_pdf,
            output_path=output_pdf,
        )

        typer.secho(
            f"✅ Compressed PDF saved to '{output_pdf}'",
            fg=typer.colors.GREEN,
        )

    except (PDFOperationError, OutputFileError) as exc:
        typer.secho(
            f"❌ {exc}",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)