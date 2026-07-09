from pathlib import Path

import typer

from ultimate_pdf.core.encryptor import decrypt_pdf


def decrypt(
    input_file: Path = typer.Argument(
        ...,
        help="Encrypted PDF file to decrypt.",
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        help="Password used to decrypt the PDF.",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output decrypted PDF.",
    ),
):
    """
    Decrypt a PDF using password of an encrypted file.
    """

    try:
        decrypt_pdf(
            input_file=input_file,
            output_file=output,
            password=password,
        )

        typer.secho(
            "✅ PDF decrypted successfully.",
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