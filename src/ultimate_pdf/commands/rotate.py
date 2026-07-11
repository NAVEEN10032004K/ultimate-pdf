from pathlib import Path

import typer

from ultimate_pdf.core.exceptions import UltimatePDFError
from ultimate_pdf.core.rotator import rotate_pdf

def rotate(
    input_file: Path = typer.Argument(
        ...,
        help="PDF file to rotate.",
    ),
    angle: int = typer.Option(
        ...,
        "--angle",
        "-a",
        help="Rotation angle (90, 180, or 270).",
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
        help="Comma-separated page numbers to rotate (example: 1,3,5). Rotates all pages if omitted.",
    ),
):
    """
    Rotate pages in a PDF.
    """

    try:
        selected_pages = None

        if pages:
            try:
                selected_pages = [
                    int(page.strip())
                    for page in pages.split(",")
                    if page.strip()
                ]
            except ValueError:
                raise typer.BadParameter(
                    "Pages must be a comma-separated list of integers "
                    "(example: 1,3,5)."
                )

        rotate_pdf(
            input_file=input_file,
            output_file=output,
            angle=angle,
            pages=selected_pages,
        )

        if selected_pages is None:
            typer.secho(
                "✅ Successfully rotated all pages.",
                fg=typer.colors.GREEN,
            )
        else:
            typer.secho(
                f"✅ Successfully rotated {len(selected_pages)} page(s).",
                fg=typer.colors.GREEN,
            )

    except typer.BadParameter as e:
        typer.secho(
            f"❌ {e}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    except UltimatePDFError as e:
        typer.secho(
            f"❌ {e}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)