from pathlib import Path

import typer

from ultimate_pdf.core.exceptions import UltimatePDFError
from ultimate_pdf.core.markdown_exporter import export_markdown


def markdown(
    input_file: Path = typer.Argument(
        ...,
        help="PDF file to export to Markdown.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output .md file. Defaults to '<name>.md' beside the PDF.",
    ),
    pages: str | None = typer.Option(
        None,
        "--pages",
        help="Pages to export (example: 1,3,5 or 2-4). All pages if omitted.",
    ),
):
    """
    Export a PDF's text content to Markdown.
    """

    try:
        written = export_markdown(
            input_file=input_file,
            output_file=output,
            pages=pages,
        )

        typer.secho(
            f"✅ Successfully exported Markdown to '{written}'.",
            fg=typer.colors.GREEN,
        )

    except UltimatePDFError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
