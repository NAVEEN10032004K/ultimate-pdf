import typer

from ultimate_pdf.commands.merge import merge

app = typer.Typer()


@app.callback()
def main():
    """Ultimate PDF CLI."""
    pass


@app.command()
def version():
    """Show the current version."""
    typer.echo("Ultimate PDF v0.1.0")


app.command()(merge)


if __name__ == "__main__":
    app()