from pypdf import PdfReader, PdfWriter
from typer.testing import CliRunner

from ultimate_pdf.cli import app

runner = CliRunner()


def test_decrypt_command(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    protected_pdf = tmp_path / "protected.pdf"
    unlocked_pdf = tmp_path / "unlocked.pdf"

    # Create a one-page PDF
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)

    with input_pdf.open("wb") as f:
        writer.write(f)

    # Encrypt it using the CLI
    encrypt_result = runner.invoke(
        app,
        [
            "encrypt",
            str(input_pdf),
            "-p",
            "secret",
            "-o",
            str(protected_pdf),
        ],
    )

    assert encrypt_result.exit_code == 0
    assert protected_pdf.exists()

    decrypt_result = runner.invoke(
        app,
        [ 
            "decrypt",
            str(protected_pdf),
            "-p",
            "secret",
            "-o",
            str(unlocked_pdf),
        ],
    )

    assert decrypt_result.exit_code == 0
    assert unlocked_pdf.exists()

    reader = PdfReader(unlocked_pdf)
    assert not reader.is_encrypted