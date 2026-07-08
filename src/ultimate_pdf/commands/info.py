from pathlib import Path

import typer

from ultimate_pdf.core.info_extractor import get_pdf_info


def info(
    input_file: Path = typer.Argument(
        ...,
        metavar="INPUT_FILE",
        help="PDF file to inspect.",
    ),
):
    """
    Display information and metadata about a PDF file.
    """

    try:
        data = get_pdf_info(input_file)

        encrypted_display = "Yes" if data["encrypted"] else "No"

        typer.echo(f"File: {data['file_name']}")
        typer.echo(f"Pages: {data['pages']}")
        typer.echo(f"Encrypted: {encrypted_display}")
        typer.echo(f"Author: {data['author']}")
        typer.echo(f"Creator: {data['creator']}")
        typer.echo(f"Producer: {data['producer']}")
        typer.echo(f"PDF Version: {data['pdf_version']}")

    except FileNotFoundError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    except Exception as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)