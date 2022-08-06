import ast
import traceback

from dbuilder import Engine


def compile(contract, print_=True):
    state, code, err = safe_compile(contract)
    if print_:
        # line cleaner
        print()
        print(code)
    if state == 0:
        print(err)
    assert state == 1


def safe_compile(contract):
    Engine.VERBOSE = 1
    t = Engine.patched(contract)
    try:
        compiled = Engine.compile(t)
        code = compiled.to_func()
        return 1, code, None
    except Exception:
        c_ast = Engine._cache[contract.__name__]
        g_src = ast.unparse(c_ast)
        err = traceback.format_exc()
        return 0, g_src, err
