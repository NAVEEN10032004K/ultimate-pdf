from pathlib import Path

import typer

from ultimate_pdf.core.encryptor_decryptor import encrypt_pdf


def encrypt(
    input_file: Path = typer.Argument(
        ...,
        help="PDF file to encrypt.",
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        help="Password used to encrypt the PDF.",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output encrypted PDF.",
    ),
):
    """
    Encrypt a PDF using a password.
    """

    try:
        encrypt_pdf(
            input_file=input_file,
            output_file=output,
            password=password,
        )

        typer.secho(
            "✅ PDF encrypted successfully.",
            fg=typer.colors.GREEN,
        )

        typer.echo(f"📁 Output: {output}")

    except FileNotFoundError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    except ValueError as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    except Exception as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)