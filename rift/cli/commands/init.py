from os.path import join as pjoin

import click

from rift.cli.entry import entry
import subprocess

templates = {
    "bare": "https://github.com/sky-ring/rift-bare-template",
    "func": "https://github.com/sky-ring/rift-func-template",
}


@entry.command(help="Initializes a new rift project at the given path")
@click.option(
    "-b",
    "--base",
    default="bare",
    help="base for the contracts",
    type=click.Choice(list(templates.keys())),
)
@click.option("-p", "--path", default=".", help="base path")
@click.argument("name")
def init(name, path, base):
    click.echo("Initializing new rift project ...")

    repo = templates[base]
    base_n = click.style(base, bold=True, italic=True, fg="magenta")
    repo_n = click.style(repo, bold=True, italic=True, fg="magenta")
    click.echo(f"Getting template {base_n} from {repo_n}")

    pt = pjoin(path, name)
    p = subprocess.run(["git", "clone", repo, pt], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode == 0:
        click.echo(click.style("Successfully created project!", fg="green"))
    else:
        click.echo(
            click.style("Error creating project!", fg="red"),
        )
        click.echo(
            click.style(p.stderr.decode("utf-8"), fg="red"),
        )
