import ast
import inspect

from dbuilder.ast import CallStacks, CompiledContract, patch
from dbuilder.core import (
    Entity,
    is_asm,
    is_impure,
    is_inline,
    is_inline_ref,
    is_method,
    is_method_id,
)
from dbuilder.core.utils import init_abstract_type


class Engine(object):
    """Engine responsible for compiling contracts."""

    VERBOSE = 0
    _cache = {}

    @staticmethod
    def compile(contract):
        inst = contract()
        CallStacks.declare_contract(contract.__name__)
        setattr(inst, "__intercepted__", True)
        attrs = dir(contract)
        d = zip(attrs, [getattr(contract, attr) for attr in attrs])
        for name, value in d:
            if name == "__annotations__":
                # TODO: Handle global and state variables
                pass
            if is_method(value):
                func_args = value.__args__
                names = value.__names__
                annots = value.__annotations__
                annots = annots if annots else {}
                args = (
                    init_abstract_type(annots.get(arg, Entity), name=arg)
                    for arg in names[1:]
                )
                annots["_method"] = {
                    "impure": is_impure(value),
                    "inline": is_inline(value),
                    "inline_ref": is_inline_ref(value),
                    "method_id": is_method_id(value),
                    "method_id_v": getattr(value, "__method_id_val__", None),
                }
                CallStacks.declare_method(
                    name,
                    [names[i + 1] for i in range(func_args - 1)],
                    annots,
                )
                value(inst, *args, NO_INTERCEPT=1)
                CallStacks.end_method(name)
            elif is_asm(value):
                func_args = value.__args__
                names = value.__names__
                annots = value.__annotations__
                asm_annots = value.__asm_annotations__
                annots = annots if annots else {}
                args = (
                    init_abstract_type(annots.get(arg, Entity), name=arg)
                    for arg in names[1:]
                )
                annots["_method"] = {
                    "impure": is_impure(value),
                    "inline": is_inline(value),
                    "inline_ref": is_inline_ref(value),
                    "method_id": is_method_id(value),
                    "method_id_v": getattr(value, "__method_id_val__", None),
                }
                CallStacks.declare_asm(
                    name,
                    [names[i + 1] for i in range(func_args - 1)],
                    annots,
                    asm_annots,
                )
                value(inst, *args, NO_INTERCEPT=1)
                CallStacks.end_method(name)

        contract_ = CallStacks.get_contract(contract.__name__)
        return CompiledContract(contract_)

    @staticmethod
    def patch(contract, _globals):
        lines, starting = inspect.findsource(contract)
        needed_src = "".join(lines[:starting])
        x = ast.parse(needed_src)
        m = {**_globals}
        exec(compile(x, "func-imports", "exec"), m)
        src = inspect.getsource(contract)
        x = ast.parse(src)
        patched_ast = patch(x)
        if Engine.VERBOSE > 0:
            Engine._cache[contract.__name__] = patched_ast
        exec(compile(patched_ast, "func-patching", "exec"), m)
        return m[contract.__name__]

    @staticmethod
    def is_patched(contract):
        return hasattr(contract, "__is_patched__") and contract.__is_patched__

    @staticmethod
    def patched(contract):
        if Engine.is_patched(contract):
            return contract
        t_globals = inspect.stack()[1][0].f_globals
        patched = Engine.patch(contract, t_globals)
        patched.__is_patched__ = True
        return patched
