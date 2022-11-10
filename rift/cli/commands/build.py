import ast
import re
import sys
from importlib.util import module_from_spec, spec_from_file_location
from os import getcwd, path

import click

from rift import Engine
from rift.cli.config import ContractConfig, ProjectConfig
from rift.cli.entry import entry
from rift.cli.util.dag import topological
from rift.cli.util.dir_util import clear_contents
from rift.cst.cst_visitor import relative_imports
from rift.func.meta_contract import ContractMeta
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
        f"Building {click.style(target, 'yellow')} from {click.style(config.name, 'blue')} project ..."
    )

    contracts_dir = path.join(cwd, "contracts")
    build_dir = path.join(cwd, "build")

    if not keep:
        clear_contents(build_dir)
    # we want to extract references and go in DAG topological order
    build_target(
        target,
        config.contracts[target],
        contracts_dir,
        build_dir,
        save_patches=log_patches,
    )


def create_save_callback(name: str, contract_name: str, build_directory: str):
    def save_patch(src):
        nonlocal name, contract_name, build_directory
        src = ast.unparse(src)
        f_x = open(path.join(build_directory, f"{name}.patched.py"), "w")
        f_x.write(src)
        f_x.close()
        click.echo(
            f"Patched {contract_name} -> build/{name}.patched.py",
        )

    return save_patch


def target_contracts(reference_graph: list):
    # we maintain the order
    t_order = topological(reference_graph)
    c_order = {v: i for i, v in enumerate(t_order)}
    # Fix missing links (isolated nodes)
    modules = [x.__module__ for x in ContractMeta.contracts]
    for m in modules:
        if m not in c_order:
            c_order[m] = len(c_order)
    # we filter the contracts and sort them as in order
    contracts = filter(
        lambda x: x.__bases__ != (object,),
        ContractMeta.contracts,
    )
    contracts = list(contracts)
    contracts = sorted(contracts, key=lambda c: c_order[c.__module__])
    # Filter out those modules that exist as sub-modules too (because of python import)
    contracts = list(
        filter(
            lambda c: "." not in c.__module__,
            contracts,
        ),
    )
    return contracts


def build_target(
    target: str,
    target_config: ContractConfig,
    contracts_dir: str,
    build_dir: str,
    log=True,
    save_patches=True,
):
    reference_graph = []
    module_globals = {}
    module_rel_imps = {}

    compile_target = target.replace("-", "_")
    process_queue = [compile_target]

    while len(process_queue) > 0:
        tg = process_queue.pop(0)
        fp = path.join(contracts_dir, tg + ".py")
        mod_name = tg

        module, imports, refs = load_module(fp, mod_name)
        module_rel_imps[mod_name] = imports
        module_globals[mod_name] = module.__dict__
        reference_graph = [*reference_graph, *refs]
        imported_ones = [x[1] for x in refs]
        process_queue.extend(imported_ones)

    contracts = target_contracts(reference_graph)
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

        name = target_config.name
        if name is None:
            name = contract.__name__
            # CamelCase -> snake_case
            name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

        callback = create_save_callback(name, contract.__name__, build_dir)
        callback = callback if save_patches else None

        is_target = contract.__name__ == target_config.contract
        t = Engine.patch(contract, tg_dict, src_callback=callback)
        patched_ones.append(t)
        compiled = Engine.compile(t)
        fc = compiled.to_func()
        f = open(path.join(build_dir, f"{name}.fc"), "w")
        f.write(fc)
        f.close()
        add_info = ""
        if not is_target:
            add_info = click.style(" (Dependency)", fg="cyan")
        if log:
            click.echo(
                f"Built {contract.__name__} -> build/{name}.fc{add_info}"
            )
    if log:
        click.echo(click.style("Target was built successfully!", fg="green"))


def load_module(file_path: str, module_name: str):
    spec = spec_from_file_location(
        module_name,
        file_path,
        submodule_search_locations=[],
    )
    mod = module_from_spec(spec)
    f = open(file_path, "r")
    code = f.read()
    code = Engine.cst_patch(code)
    mod.__file__ = file_path
    sys.modules[module_name] = mod

    imp_ = relative_imports(code)
    full_imports = imp_._detailed_imports
    refs = []
    for i in full_imports:
        refs.append((module_name, i))

    compiled = compile(code, file_path, "exec")
    exec(compiled, mod.__dict__)
    return mod, full_imports, refs
