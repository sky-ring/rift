import ast
import os
import traceback
from pathlib import Path

from dbuilder import Engine
from dbuilder.ast.ref_table import ReferenceTable


def write(target: str, content: str):
    p = Path(target)
    if not p.parent.exists():
        os.makedirs(p.parent.absolute(), exist_ok=True)
    with open(target, "w") as f:
        f.write(content)


def compile(contract, print_=True, ast=False, file_=True):
    state, code, err = safe_compile(contract)
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


def safe_compile(contract):
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
