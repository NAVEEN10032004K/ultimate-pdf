from pathlib import Path

import typer

from ultimate_pdf.core.exceptions import UltimatePDFError
from ultimate_pdf.core.ocr import ocr_pdf


def ocr(
    input_file: Path = typer.Argument(
        ...,
        help="PDF file to run OCR on.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file. Required for 'pdf' mode; prints to stdout in 'text' mode if omitted.",
    ),
    mode: str = typer.Option(
        "pdf",
        "--mode",
        "-m",
        help="'pdf' for a searchable PDF, 'text' to extract recognized text.",
    ),
    language: str = typer.Option(
        "eng",
        "--language",
        "-l",
        help="Tesseract language code (example: eng, deu).",
    ),
    dpi: int = typer.Option(
        300,
        "--dpi",
        help="Render resolution used for OCR.",
    ),
    pages: str | None = typer.Option(
        None,
        "--pages",
        help="Pages to process (example: 1,3,5 or 2-4). All pages if omitted.",
    ),
):
    """
    Run OCR on a scanned PDF (searchable PDF or extracted text).
    """

    try:
        text = ocr_pdf(
            input_file=input_file,
            output_file=output,
            mode=mode,
            language=language,
            dpi=dpi,
            pages=pages,
        )

        if mode == "text" and output is None:
            typer.echo(text)
        else:
            typer.secho(
                f"✅ Successfully ran OCR on '{input_file}'.",
                fg=typer.colors.GREEN,
            )

    except UltimatePDFError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
