from pypdf import PdfWriter
from typer.testing import CliRunner

from ultimate_pdf.cli import app

runner = CliRunner()


def test_info_command(tmp_path):
    input_pdf = tmp_path / "input.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    with input_pdf.open("wb") as f:
        writer.write(f)

    result = runner.invoke(app, ["info", str(input_pdf)])

    assert result.exit_code == 0
    assert "Pages: 1" in result.stdout
    assert "Encrypted: No" in result.stdout
