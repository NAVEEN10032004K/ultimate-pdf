from pathlib import Path

import typer
from pypdf import PdfWriter

from pathlib import Path


def merge(
    input_files: list[Path] = typer.Argument(
        ...,
        metavar="INPUT_FILES...",
        help="One or more PDF files to merge.",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output PDF file.",
    ),
):
    """Merge multiple PDF files into one."""

    writer = PdfWriter()

    try:
        for pdf in input_files:
            if not pdf.exists():
                typer.secho(
                    f"Error: File not found: {pdf}",
                    fg=typer.colors.RED,
                )
                raise typer.Exit(code=1)

            typer.echo(f"Adding: {pdf.name}")
            writer.append(str(pdf))

        writer.write(output)
        writer.close()

        typer.secho(
            f"\n✓ Successfully merged {len(input_files)} PDF(s)",
            fg=typer.colors.GREEN,
        )
        typer.echo(f"Output: {output}")

    except Exception as e:
        writer.close()
        typer.secho(
            f"Error: {e}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)