from pathlib import Path

import typer

from ultimate_pdf.core.exceptions import UltimatePDFError
from ultimate_pdf.core.image_converter import images_to_pdf


def image_to_pdf(
    input_files: list[Path] = typer.Argument(
        ...,
        metavar="INPUT_FILES",
        help="Image files to combine into a PDF.",
    ),
    output: Path = typer.Option(
        Path("output.pdf"),
        "--output",
        "-o",
        metavar="OUTPUT",
        help="Output PDF file.",
    ),
):
    """
    Combine images into a single PDF (one image per page).
    """

    try:
        images_to_pdf(input_files, output)

        typer.secho(
            f"✅ Successfully converted {len(input_files)} image(s) into '{output}'.",
            fg=typer.colors.GREEN,
        )

    except UltimatePDFError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
