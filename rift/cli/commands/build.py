from os import getcwd, path, makedirs

import click

from rift.cli.commands.utils import build_target
from rift.cli.config import ProjectConfig
from rift.cli.entry import entry
from rift.cli.util.dir_util import clear_contents
from rift.runtime.config import FunCMode


@entry.command(help="Builds the project")
@click.option(
    "--log-patches",
    default=False,
    help="generated patched sources [for debug purposes]",
    is_flag=True,
)
@click.option(
    "--keep",
    default=False,
    help="keep contents of build/ directory",
    is_flag=True,
)
@click.argument("target")
def build(target, log_patches, keep):
    FunCMode.activate()
    cwd = getcwd()
    config = ProjectConfig.working()
    if not config:
        click.echo(
            click.style("Not a rift project!", fg="red"),
        )
        return

    click.echo(
        f"Building {click.style(target, 'yellow')} from {click.style(config.name, 'blue')} project ...",
    )

    contracts_dir = path.join(cwd, "contracts")
    build_dir = path.join(cwd, "build")
    makedirs(build_dir, mode=0o777, exist_ok=True)

    if not keep:
        clear_contents(build_dir)

    if target == "all":
        targets = list(config.contracts.keys())
    else:
        targets = [target]

    for target in targets:
        build_target(
            target,
            config.contracts[target],
            config,
            contracts_dir,
            build_dir,
            save_patches=log_patches,
        )
