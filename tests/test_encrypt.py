from pypdf import PdfReader, PdfWriter
from typer.testing import CliRunner

from ultimate_pdf.cli import app

runner = CliRunner()


def _make_pdf(path):
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    with path.open("wb") as f:
        writer.write(f)


def test_encrypt_command_success(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "protected.pdf"
    _make_pdf(input_pdf)

    result = runner.invoke(
        app,
        ["encrypt", str(input_pdf), "-p", "secret", "-o", str(output_pdf)],
    )

    assert result.exit_code == 0
    assert output_pdf.exists()

    reader = PdfReader(output_pdf)
    assert reader.is_encrypted
    assert reader.decrypt("secret") != 0


def test_encrypt_command_empty_password(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "protected.pdf"
    _make_pdf(input_pdf)

    result = runner.invoke(
        app,
        ["encrypt", str(input_pdf), "-p", "  ", "-o", str(output_pdf)],
    )

    assert result.exit_code == 1
    assert not output_pdf.exists()


def test_encrypt_command_nonexistent_input(tmp_path):
    missing_pdf = tmp_path / "missing.pdf"
    output_pdf = tmp_path / "protected.pdf"

    result = runner.invoke(
        app,
        ["encrypt", str(missing_pdf), "-p", "secret", "-o", str(output_pdf)],
    )

    assert result.exit_code == 1
    assert not output_pdf.exists()


def test_encrypt_command_invalid_extension(tmp_path):
    not_a_pdf = tmp_path / "input.txt"
    not_a_pdf.write_text("hello")
    output_pdf = tmp_path / "protected.pdf"

    result = runner.invoke(
        app,
        ["encrypt", str(not_a_pdf), "-p", "secret", "-o", str(output_pdf)],
    )

    assert result.exit_code == 1
    assert not output_pdf.exists()
