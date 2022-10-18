import ast
import os
import traceback
from pathlib import Path

from rift import Engine
from rift.ast.ref_table import ReferenceTable
from rift.fift.fift import Fift
from rift.fift.func import FunC, FunCError, FunCResult
from rift.runtime.config import Config, Mode


def write(target: str, content: str):
    p = Path(target)
    if not p.parent.exists():
        os.makedirs(p.parent.absolute(), exist_ok=True)
    with open(target, "w") as f:
        f.write(content)


def compile(contract, print_=True, ast=False, file_=True, link_std=True):
    code = compile_py(contract, print_=print_, ast=ast, file_=file_)
    program = compile_func(code, link_std=link_std)
    cell = compile_fift(program)
    return cell


def compile_fift(program):
    Config.mode = Mode.FIFT
    if "DECLPROC recv_internal" not in program:
        idx = program.find("}END>c")
        main_method = "DECLPROC recv_internal\nrecv_internal PROC:<{\n}>\n"
        program = program[:idx] + main_method + program[idx:]
    c = Fift.exec(program.strip())
    return c[0]


def compile_func(code, link_std=True):
    sources = [code]
    if link_std:
        sources.insert(0, "#stdlib")
    res = FunC.compile_source(
        *sources,
        optimization_level=0,
    )
    if isinstance(res, FunCError):
        print(res.error)
    assert isinstance(res, FunCResult)
    fift_code = res.fift_code
    return fift_code


def compile_py(contract, print_=True, ast=False, file_=True):
    Config.mode = Mode.FUNC
    state, code, err = safe_compile_py(contract)
    if ast:
        print()
        print(err)
    if print_:
        # line cleaner
        print()
        print(code)
        if file_:
            content = code if state == 1 else err
            write(f".build/{contract.__name__.lower()}.fc", content)
            patched_src = err if state == 1 else code
            write(
                f".build/{contract.__name__.lower()}.patched.py",
                patched_src,
            )
            write(
                f".build/{contract.__name__.lower()}.ref.json",
                ReferenceTable.dump(),
            )

    if state == 0:
        print(err)
    assert state == 1
    return code


def safe_compile_py(contract):
    Engine.VERBOSE = 1
    t = Engine.patched(contract)
    c_ast = Engine._cache[contract.__name__]
    g_src = ast.unparse(c_ast)
    try:
        compiled = Engine.compile(t)
        code = compiled.to_func()
        return 1, code, g_src
    except Exception:
        err = traceback.format_exc()
        return 0, g_src, err
