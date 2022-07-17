import click

from dbuilder.cli import entry
from dbuilder.cli.util import DirectoryStructure


@entry.command()
@click.argument("path")
def init(path):
    click.echo("Initializing new dbuilder project ...")

    p_dir = DirectoryStructure(path)
    p_dir << ".dbuilder"
    p_dir << "contracts"
    p_dir << "build"
    ok = p_dir.create_dirs()
    if ok:
        click.echo(click.style("Successfully created project!", fg="green"))
    else:
        click.echo(
            click.style("Error creating project, dir exists!", fg="red"),
        )
