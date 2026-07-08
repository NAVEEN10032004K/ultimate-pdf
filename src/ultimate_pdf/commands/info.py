from pathlib import Path

import typer

from ultimate_pdf.core.parser import get_pdf_info

from ultimate_pdf.core.exceptions import PDFNotFoundError, InvalidPDFError

def info(
    input_file: Path = typer.Argument(
        ...,
        metavar="INPUT_FILE",
        help="PDF file to inspect.",
    ),
):
    """
    Display information about a PDF file.
    """

    try:
        # pulls page count, encryption status, and metadata from the parser
        pdf_info = get_pdf_info(input_file)

        typer.secho("\n📄 PDF Information", fg=typer.colors.CYAN, bold=True)
        typer.echo(f"File Name : {pdf_info.file_name}")
        typer.echo(f"File Path : {pdf_info.file_path}")
        typer.echo(f"Pages     : {pdf_info.page_count}")
        typer.echo(f"Encrypted : {'Yes' if pdf_info.encrypted else 'No'}")

        typer.secho("\nMetadata", fg=typer.colors.BLUE, bold=True)
        typer.echo(f"Title     : {pdf_info.title or 'N/A'}")
        typer.echo(f"Author    : {pdf_info.author or 'N/A'}")
        typer.echo(f"Subject   : {pdf_info.subject or 'N/A'}")
        typer.echo(f"Creator   : {pdf_info.creator or 'N/A'}")
        typer.echo(f"Producer  : {pdf_info.producer or 'N/A'}")

    # catches the "file missing" / "not a real pdf" cases separately so we
    # can show a clean message instead of a scary traceback
    except (PDFNotFoundError, InvalidPDFError) as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # catch-all for anything else that goes wrong while reading the file
    except Exception as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)