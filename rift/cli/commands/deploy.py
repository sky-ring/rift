from os import getcwd, path

import click

from rift.cli.config import ContractConfig, ProjectConfig
from rift.cli.entry import entry
from rift.runtime.config import FiftMode


@entry.command(help="Deploys an specific target")
@click.argument("target")
def deploy(target):
    FiftMode.activate()
    cwd = getcwd()
    config = ProjectConfig.working()
    if not config:
        click.echo(
            click.style("Not a rift project!", fg="red"),
        )
        return

    click.echo(
        f"Deploying {click.style(target, 'yellow')} from {click.style(config.name, 'blue')} project ..."
    )

    contracts_dir = path.join(cwd, "deployers")
    build_dir = path.join(cwd, "build")
