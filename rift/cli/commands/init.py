from os.path import join as pjoin

import click
from tomlkit import comment, document, nl

from rift.bases import write_contract
from rift.cli.entry import entry
from rift.cli.util import DirectoryStructure


@entry.command(help="Initializes a new rift project at the given path")
@click.option(
    "-b",
    "--base",
    default="bare",
    help="base for the contracts",
    type=click.Choice(["bare"]),
)
@click.option("-p", "--path", default=".", help="base path")
@click.argument("name")
def init(name, path, base):
    click.echo("Initializing new rift project ...")

    p_dir = DirectoryStructure(pjoin(path, name))
    p_dir << "contracts"
    p_dir << "build"
    ok = p_dir.create_dirs()
    if ok:
        write_contract(base, pjoin(path, name, "contracts", f"{name}.py"))

        doc = document()
        doc.add(comment("rift project configuration file"))
        doc.add(nl())
        doc["name"] = name
        r = doc.as_string()
        f = open(pjoin(path, name, "project.toml"), "w")
        f.write(r)
        f.close()

        click.echo(click.style("Successfully created project!", fg="green"))
    else:
        click.echo(
            click.style("Error creating project, dir exists!", fg="red"),
        )
