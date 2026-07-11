from pypdf import PdfReader, PdfWriter
from typer.testing import CliRunner

from ultimate_pdf.cli import app

runner = CliRunner()


def _make_pdf(path, pages=1):
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=595, height=842)
    with path.open("wb") as f:
        writer.write(f)


def test_compress_command_success(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    _make_pdf(input_pdf, pages=3)

    result = runner.invoke(app, ["compress", str(input_pdf), "-o", str(output_pdf)])

    assert result.exit_code == 0
    assert output_pdf.exists()

    reader = PdfReader(output_pdf)
    assert len(reader.pages) == 3


def test_compress_command_default_output_name(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    _make_pdf(input_pdf)

    result = runner.invoke(app, ["compress", str(input_pdf)])

    assert result.exit_code == 0
    assert (tmp_path / "input_compressed.pdf").exists()


def test_compress_command_nonexistent_input(tmp_path):
    missing_pdf = tmp_path / "missing.pdf"

    result = runner.invoke(app, ["compress", str(missing_pdf)])

    assert result.exit_code != 0


def test_compress_command_invalid_extension(tmp_path):
    not_a_pdf = tmp_path / "input.txt"
    not_a_pdf.write_text("hello")

    result = runner.invoke(app, ["compress", str(not_a_pdf)])

    assert result.exit_code == 1
