from typer.testing import CliRunner

from ultimate_pdf.cli import app

runner = CliRunner()


def test_info_command():
    result = runner.invoke(
        app,
        ["info", "paper.pdf"],
    )

    assert result.exit_code == 0
    assert "PDF Information" in result.stdout
