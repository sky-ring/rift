import ast
import re
import sys
from importlib.util import module_from_spec, spec_from_file_location
from os import path

import click

from rift import Engine
from rift.cli.config import ContractConfig, ProjectConfig
from rift.cli.util.dag import topological
from rift.cst.cst_visitor import relative_imports
from rift.fift.fift import Fift, FiftError
from rift.fift.func import FunC, FunCError, FunCResult
from rift.func.meta_contract import ContractMeta
from rift.runtime.config import FiftMode


def build_target(
    target: str,
    target_config: ContractConfig,
    config: ProjectConfig,
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
    contract_files = {}
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

        name = config.get_contract_file_name(contract)

        callback = create_save_callback(name, contract.__name__, build_dir)
        callback = callback if save_patches else None

        is_target = contract.__name__ == target_config.contract

        # We check whether contract is prebuilt or not
        fc = contract.__fc_code__
        if fc is not None:
            # It's prebuilt
            if isinstance(fc, tuple) or isinstance(fc, list):
                fc = list(fc)
            else:
                fc = [fc]
            files = [path.join(contracts_dir, f) for f in fc]
            if log:
                click.echo(
                    f"Detected prebuilt contract {contract.__name__}",
                )
        else:
            # It's not prebuilt so let's patch it up and compile it to FunC
            t = Engine.patch(contract, tg_dict, src_callback=callback)
            patched_ones.append(t)
            compiled = Engine.compile(t)
            fc = compiled.to_func()
            fc_file = path.join(build_dir, f"{name}.fc")
            write_file(fc_file, fc)
            contract_files[contract.__name__] = fc_file
            add_info = ""
            if not is_target:
                add_info = click.style(" (Dependency)", fg="cyan")
            if log:
                click.echo(
                    f"Built {contract.__name__} -> build/{name}.fc{add_info}",
                )
            # Acquire dependency -> compile link func
            # We need dependencies here to link against them
            contract_classes = [v.contract for v in config.contracts.values()]
            deps = [
                v for k, v in contract_files.items() if k not in contract_classes
            ]
            files = [*deps, fc_file]
        ok, res = compile_func(files)
        if ok:
            name_styled = click.style(name)
            write_file(path.join(build_dir, f"{name}.fif"), res)
            click.echo(
                f"Compiled {name_styled}.fc -> build/{name}.fif",
            )
            try:
                c = compile_fift(res, patch_methods=False)
                write_file(
                    path.join(build_dir, f"{name}.boc"),
                    bytes(c),
                    mode="wb",
                )
                click.echo(
                    f"Assembled {name_styled}.fif -> build/{name}.boc",
                )
                c_patched = compile_fift(res, patch_methods=True)
                write_file(
                    path.join(build_dir, f"{name}.patched.boc"),
                    bytes(c_patched),
                    mode="wb",
                )
                test_tag = click.style("[Testing]", fg="yellow", italic=True)
                click.echo(
                    f"Assembled {name_styled}.fif -> build/{name}.patched.boc {test_tag}",
                )
            except FiftError as fe:
                click.echo(
                    f"Failure during assembling of {name_styled}.fif",
                )
                click.secho(fe.msg, fg="red")
        else:
            name_styled = click.style(name)
            click.echo(
                f"Failure during compilation of {name_styled}.fc to fift",
            )
            click.secho(res, fg="red")

    if log:
        click.echo(click.style("Target was built successfully!", fg="green"))
    contract_objects = {p.__name__: p for p in patched_ones}
    return contract_objects


def load_module(file_path: str, module_name: str, patch=True):
    spec = spec_from_file_location(
        module_name,
        file_path,
        submodule_search_locations=[],
    )
    mod = module_from_spec(spec)
    f = open(file_path, "r")
    code = f.read()
    if patch:
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


def compile_fift(program, patch_methods=False):
    FiftMode.activate()
    c = Fift.assemble(program, fix_main=True, patch_methods=patch_methods)
    return c


def compile_func(target_files, link_std=True):
    links = []
    if link_std:
        links.append("#stdlib")
    res = FunC.compile_link(
        target_files,
        links,
        optimization_level=2,
    )
    if isinstance(res, FunCError):
        return False, res.error
    fift_code = res.fift_code
    return True, fift_code


def write_file(fp, content, mode="w"):
    with open(fp, mode) as f:
        f.write(content)
