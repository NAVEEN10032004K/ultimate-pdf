from pypdf import PdfReader, PdfWriter
from typer.testing import CliRunner

from ultimate_pdf.cli import app

runner = CliRunner()


def test_encrypt_command(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "protected.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)

    with input_pdf.open("wb") as f:
        writer.write(f)

    result = runner.invoke(
        app,
        [
            "encrypt",
            str(input_pdf),
            "-p",
            "secret",
            "-o",
            str(output_pdf),
        ],
    )

    assert result.exit_code == 0
    assert output_pdf.exists()

    reader = PdfReader(output_pdf)
    assert reader.is_encrypted