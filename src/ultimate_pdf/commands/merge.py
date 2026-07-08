from pathlib import Path

import typer

from ultimate_pdf.core.merger import merge_pdfs


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
    """
    Merge multiple PDF files into one.
    """

    try:
        merge_pdfs(input_files, output)

        typer.secho(
            f"✅ Successfully merged {len(input_files)} PDF file(s)",
            fg=typer.colors.GREEN,
        )
        typer.echo(f"📁 Output: {output}")

    except FileNotFoundError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    except Exception as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)