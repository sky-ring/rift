import re
import sys
from os import getcwd, listdir
from os.path import exists as p_exists
from os.path import join as p_join
from types import ModuleType

import click
from tomlkit import parse

from dbuilder import Engine
from dbuilder.cli import entry
from dbuilder.func.meta_contract import ContractMeta


@entry.command(help="Builds the project")
def build():
    cwd = getcwd()
    config_file = p_join(cwd, "project.toml")
    if not p_exists(config_file):
        click.echo(
            click.style("Not a dbuilder project!", fg="red"),
        )
        return
    f = open(config_file, "r")
    doc = parse(f.read())
    click.echo(f"Building {doc['name']} project ...")

    c_dir = p_join(cwd, "contracts")
    for cf in listdir(c_dir):
        mod_name = cf.replace(".py", "")
        mod = ModuleType(mod_name)
        fp = p_join(c_dir, cf)
        f = open(fp, "r")
        code = f.read()
        mod.__file__ = fp
        sys.modules[mod_name] = mod
        compiled = compile(code, fp, "exec")
        exec(compiled, mod.__dict__)
        click.echo(f"compiling {cf}")

    b_dir = p_join(cwd, "build")
    for contract in [*ContractMeta.contracts]:
        if contract.__bases__ != (object,):
            module = sys.modules.get(contract.__module__)
            t = Engine.patch(contract, module.__dict__)
            compiled = Engine.compile(t)
            fc = compiled.to_func()
            name = contract.__name__
            name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
            f = open(p_join(b_dir, f"{name}.fc"), "w")
            f.write(fc)
            f.close()
            click.echo(f"Built {contract.__name__} -> build/{name}.fc")
    click.echo(click.style("Project was built successfully!", fg="green"))
