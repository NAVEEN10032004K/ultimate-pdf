import typer

app = typer.Typer()


@app.callback()
def main():
    """Ultimate PDF CLI."""
    pass


@app.command()
def version():
    """Show the current version."""
    print("Ultimate PDF v0.1.0")


if __name__ == "__main__":
    app()