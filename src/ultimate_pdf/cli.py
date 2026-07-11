from importlib.metadata import version as _pkg_version

import typer

from ultimate_pdf.commands.merge import merge
from ultimate_pdf.commands.split import split
from ultimate_pdf.commands.info import info
from ultimate_pdf.commands.encrypt import encrypt
from ultimate_pdf.commands.decrypt import decrypt
from ultimate_pdf.commands.rotate import rotate
from ultimate_pdf.commands.compress import compress
from ultimate_pdf.commands.pdf_to_image import pdf_to_image
from ultimate_pdf.commands.image_to_pdf import image_to_pdf
from ultimate_pdf.commands.watermark import watermark
from ultimate_pdf.commands.ocr import ocr
from ultimate_pdf.commands.markdown import markdown

app = typer.Typer()


@app.callback()
def main():
    """Ultimate PDF CLI."""
    pass


@app.command()
def version():
    """Show the current version."""
    typer.echo(f"Ultimate PDF v{_pkg_version('ultimate-pdf')}")


app.command()(merge)
app.command()(split)
app.command()(info)
app.command()(encrypt)
app.command()(decrypt)
app.command()(rotate)
app.command()(compress)
app.command()(pdf_to_image)
app.command()(image_to_pdf)
app.command()(watermark)
app.command()(ocr)
app.command()(markdown)

if __name__ == "__main__":
    app()