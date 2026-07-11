from typer.testing import CliRunner

from ultimate_pdf.cli import app

runner = CliRunner()


def test_version_command():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "Ultimate PDF" in result.stdout
