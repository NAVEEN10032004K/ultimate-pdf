from pathlib import Path

import typer

from ultimate_pdf.core.exceptions import UltimatePDFError
from ultimate_pdf.core.info_extractor import extract_pdf_info

import logging

logging.getLogger("pypdf").setLevel(logging.ERROR)
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
        data = extract_pdf_info(input_file)

        encrypted_display = "Yes" if data["encrypted"] else "No"

        typer.echo(f"File: {data['file_name']}")
        typer.echo(f"Path: {data['file_path']}")
        typer.echo(f"Pages: {data['pages']}")
        typer.echo(f"Encrypted: {encrypted_display}")
        typer.echo(f"Title: {data['title'] or 'Unknown'}")
        typer.echo(f"Author: {data['author']}")
        typer.echo(f"Subject: {data['subject'] or 'Unknown'}")
        typer.echo(f"Creator: {data['creator']}")
        typer.echo(f"Producer: {data['producer']}")
        typer.echo(f"PDF Version: {data['pdf_version']}")

    except UltimatePDFError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    except Exception as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)