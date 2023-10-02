import os

import click

from theTrial import __version__


SETTINGS_INITIAL_CONTENT = """# settings.py

CONFIG_CONSUMER = {
    "bootstrap.servers": "" # add broker url here,
}


CONFIG_PRODUCER = {
    "bootstrap.servers": "" # add broker url here,
}
"""

MODELS_INITIAL_CONTENT = """from pydantic import BaseModel

# add your models here
"""


def create_file(path: str, filename: str, content: str = "") -> None:
    """Create a file with the specified content at the given path and filename."""
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), "w") as file:
        file.write(content)


@click.group(help=f"theTrial CLI Tool v{__version__}")
@click.version_option(version=__version__, prog_name="theTrial")
def main():
    pass


@click.command()
@click.option("--name", default="app", help="Name of the main app file file.")
def start(name: str) -> None:
    """Initialize a new project structure."""

    create_file(os.getcwd(), name + ".py")
    click.echo("[INFO] Main app file created.")

    create_file(os.getcwd(), "settings.py", SETTINGS_INITIAL_CONTENT)
    click.echo("[INFO] Settings.py file created.")

    create_file(os.path.join(os.getcwd(), "models"), "__init__.py")
    create_file(
        os.path.join(os.getcwd(), "models"), "models.py", MODELS_INITIAL_CONTENT
    )
    click.echo("[INFO] Models directory and its files created.")

    click.echo("✅")


main.add_command(start)

if __name__ == "__main__":
    main()
