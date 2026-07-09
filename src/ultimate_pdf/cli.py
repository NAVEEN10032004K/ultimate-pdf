import typer

from ultimate_pdf.commands.merge import merge
from ultimate_pdf.commands.split import split
from ultimate_pdf.commands.info import info  
from ultimate_pdf.commands.encrypt import encrypt
from ultimate_pdf.commands.decrypt import decrypt

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
app.command()(split)
app.command()(info)  
app.command()(encrypt)
app.command()(decrypt)

if __name__ == "__main__":
    app()