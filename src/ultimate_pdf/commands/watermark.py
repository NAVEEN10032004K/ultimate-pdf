from pathlib import Path

import typer

from ultimate_pdf.core.exceptions import UltimatePDFError
from ultimate_pdf.core.watermarker import add_image_watermark, add_text_watermark


def watermark(
    input_file: Path = typer.Argument(
        ...,
        help="PDF file to watermark.",
    ),
    text: str | None = typer.Option(
        None,
        "--text",
        help="Text watermark to stamp on each page.",
    ),
    image: Path | None = typer.Option(
        None,
        "--image",
        help="Image watermark to stamp on each page.",
    ),
    opacity: float = typer.Option(
        0.15,
        "--opacity",
        help="Watermark opacity (0.0 - 1.0).",
    ),
    rotate: int = typer.Option(
        0,
        "--rotate",
        help="Text rotation (0, 90, 180, or 270).",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output PDF file.",
    ),
    pages: str | None = typer.Option(
        None,
        "--pages",
        help="Pages to watermark (example: 1,3,5 or 2-4). All pages if omitted.",
    ),
):
    """
    Add a text or image watermark to a PDF.
    """

    if bool(text) == bool(image):
        typer.secho(
            "❌ Provide exactly one of --text or --image.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    try:
        if text:
            add_text_watermark(
                input_file=input_file,
                output_file=output,
                text=text,
                opacity=opacity,
                rotate=rotate,
                pages=pages,
            )
        else:
            add_image_watermark(
                input_file=input_file,
                output_file=output,
                image=image,
                opacity=opacity,
                pages=pages,
            )

        typer.secho(
            f"✅ Successfully watermarked '{output}'.",
            fg=typer.colors.GREEN,
        )

    except UltimatePDFError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
