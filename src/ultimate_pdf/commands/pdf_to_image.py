from pathlib import Path

import typer

from ultimate_pdf.core.exceptions import UltimatePDFError
from ultimate_pdf.core.rasterizer import pdf_to_images


def pdf_to_image(
    input_file: Path = typer.Argument(
        ...,
        help="PDF file to convert to images.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Directory for the images. Defaults to '<name>_images' beside the PDF.",
    ),
    dpi: int = typer.Option(
        200,
        "--dpi",
        help="Render resolution in DPI.",
    ),
    fmt: str = typer.Option(
        "png",
        "--format",
        "-f",
        help="Image format (png, jpg, ...).",
    ),
    pages: str | None = typer.Option(
        None,
        "--pages",
        help="Pages to convert (example: 1,3,5 or 2-4). Converts all pages if omitted.",
    ),
):
    """
    Convert PDF pages into image files.
    """

    try:
        count = pdf_to_images(
            input_file=input_file,
            output_dir=output_dir,
            dpi=dpi,
            fmt=fmt,
            pages=pages,
        )

        typer.secho(
            f"✅ Successfully converted {count} page(s) to images.",
            fg=typer.colors.GREEN,
        )

    except UltimatePDFError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
