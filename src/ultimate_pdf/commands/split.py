from pathlib import Path

import typer

from ultimate_pdf.core.splitter import (
    split_every_n_pages,
    split_page_range,
    split_selected_pages,
    split_to_pages,
)

app = typer.Typer()


@app.command()
def split(
    input_file: Path = typer.Argument(
        ...,
        help="PDF file to split.",
    ),
    pages: str | None = typer.Option(
        None,
        "--pages",
        help="Page range (example: 5-10).",
    ),
    every: int | None = typer.Option(
        None,
        "--every",
        help="Split every N pages.",
    ),
    select: str | None = typer.Option(
        None,
        "--select",
        help="Selected pages (example: 1,3,8).",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output PDF (required for --pages and --select).",
    ),
):
    """
    Split PDF files.
    """

    try:

        # Split into individual pages
        if not pages and not every and not select:
            count = split_to_pages(input_file)

            typer.secho(
                f"✅ Split into {count} individual pages.",
                fg=typer.colors.GREEN,
            )
            return

        # Split page range
        if pages:

            if output is None:
                raise typer.BadParameter("--output is required when using --pages.")

            start, end = map(int, pages.split("-"))

            split_page_range(
                input_file,
                start,
                end,
                output,
            )

            typer.secho(
                "✅ Page range extracted successfully.",
                fg=typer.colors.GREEN,
            )
            return

        # Split every N pages
        if every:

            files = split_every_n_pages(
                input_file,
                every,
            )

            typer.secho(
                f"✅ Created {files} PDF files.",
                fg=typer.colors.GREEN,
            )
            return

        # Split selected pages
        if select:

            if output is None:
                raise typer.BadParameter("--output is required when using --select.")

            selected_pages = [int(page.strip()) for page in select.split(",")]

            split_selected_pages(
                input_file,
                selected_pages,
                output,
            )

            typer.secho(
                "✅ Selected pages extracted successfully.",
                fg=typer.colors.GREEN,
            )

    except Exception as e:
        typer.secho(
            f"❌ {e}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)
