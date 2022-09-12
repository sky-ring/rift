import ast
import re
import sys
from importlib.util import module_from_spec, spec_from_file_location
from os import getcwd, listdir
from os.path import exists as p_exists
from os.path import join as p_join

import click
from tomlkit import parse

from rift import Engine
from rift.cli.entry import entry
from rift.cli.util.dag import topological
from rift.cli.util.dir_util import clear_contents
from rift.cst.cst_visitor import relative_imports
from rift.func.meta_contract import ContractMeta


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
def build(log_patches, keep):
    cwd = getcwd()
    config_file = p_join(cwd, "project.toml")
    if not p_exists(config_file):
        click.echo(
            click.style("Not a rift project!", fg="red"),
        )
        return
    f = open(config_file, "r")
    doc = parse(f.read())
    click.echo(f"Building {doc['name']} project ...")

    c_dir = p_join(cwd, "contracts")
    # we want to extract references and go in DAG topological order
    refs = []
    allowed_modules = []
    module_globals = {}
    module_rel_imps = {}
    for cf in listdir(c_dir):
        if not cf.endswith(".py"):
            continue
        mod_name = cf.replace(".py", "")
        fp = p_join(c_dir, cf)
        spec = spec_from_file_location(
            mod_name,
            fp,
            submodule_search_locations=[],
        )
        mod = module_from_spec(spec)
        f = open(fp, "r")
        code = f.read()
        code = Engine.cst_patch(code)
        mod.__file__ = fp
        sys.modules[mod_name] = mod
        # gather refs
        imp_ = relative_imports(code)
        module_rel_imps[mod_name] = imp_._detailed_imports
        for i in imp_._relative_accesses:
            refs.append((mod_name, i))
        compiled = compile(code, fp, "exec")
        exec(compiled, mod.__dict__)
        module_globals[mod_name] = mod.__dict__
        allowed_modules.append(mod_name)
        click.echo(f"compiling {cf}")
    b_dir = p_join(cwd, "build")
    if not keep:
        clear_contents(b_dir)
    # we maintain the order
    t_order = topological(refs)
    c_order = {v: i for i, v in enumerate(t_order)}
    # we filter the contracts and sort them as in order
    contracts = filter(
        lambda x: x.__bases__ != (object,),
        ContractMeta.contracts,
    )
    contracts = filter(
        lambda x: x.__module__ in allowed_modules,
        ContractMeta.contracts,
    )
    contracts = list(contracts)
    contracts = sorted(contracts, key=lambda c: c_order[c.__module__])
    patched_ones = []
    for contract in contracts:
        module = sys.modules.get(contract.__module__)
        tg_dict = {**module.__dict__}
        for m, imps in module_rel_imps[contract.__module__].items():
            # here we have any relative import this contract has
            # imp_d is a dict imported_module -> [imported_classses]
            for i in imps:
                tg_dict[i] = module_globals[m][i]
        for p in patched_ones:
            # what we do is provide new patched instances
            # instead of old ones (imported)
            tg_dict[p.__name__] = p

        name = None
        c = doc.get("contracts")
        if c is not None:
            ct = c.get(contract.__name__)
            if ct is not None:
                name = ct.get("name")
        if name is None:
            name = contract.__name__
            name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

        def save_patch(src):
            if not log_patches:
                return
            nonlocal name
            src = ast.unparse(src)
            f_x = open(p_join(b_dir, f"{name}.patched.py"), "w")
            f_x.write(src)
            f_x.close()
            click.echo(
                f"Patched {contract.__name__} -> build/{name}.patched.py",
            )

        t = Engine.patch(contract, tg_dict, src_callback=save_patch)
        patched_ones.append(t)
        compiled = Engine.compile(t)
        fc = compiled.to_func()

        f = open(p_join(b_dir, f"{name}.fc"), "w")
        f.write(fc)
        f.close()
        click.echo(f"Built {contract.__name__} -> build/{name}.fc")
    click.echo(click.style("Project was built successfully!", fg="green"))
