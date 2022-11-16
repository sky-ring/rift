import sys
from os import getcwd, path

import click

from rift.cli.commands.utils import load_module
from rift.cli.config import ProjectConfig
from rift.cli.entry import entry
from rift.fift.types import Cell
from rift.func.meta_contract import ContractMeta
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
        f"Deploying {click.style(target, 'yellow')} from {click.style(config.name, 'blue')} project ...",
    )

    contracts_dir = path.join(cwd, "deployers")
    build_dir = path.join(cwd, "build")

    contract_config = config.contracts[target]
    compile_target = contract_config.deploy
    if compile_target is None:
        click.secho(
            "Target doesn't have a deploy script!",
            fg="red",
        )
    fp = path.join(contracts_dir, compile_target + ".py")

    sys.path.append(cwd)
    mod, *_ = load_module(fp, compile_target, patch=False)
    print(mod)
    # print(mod.__dict__)
    contracts = ContractMeta.defined_contracts()

    for contract in contracts:
        contract_cfg = config.get_contract(contract.__name__)
        name = contract_cfg.get_file_name()
        boc_file = path.join(build_dir, f"{name}.boc")
        if not path.exists(boc_file):
            click.secho(
                f"Couldn't find {name}.boc, Have you built the target? (rift build <target>)",
                fg="red",
            )
            return
        code_cell = Cell.load_from(boc_file)
        contract.__code_cell__ = code_cell

    mod.deploy()

    # TODO:
    # Inject built code from the dir into it
    # If it's not built, error and suggest build command
    # Proceed with running the function
