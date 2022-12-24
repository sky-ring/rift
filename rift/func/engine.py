import ast
import inspect
import textwrap

import yaml

from rift.ast import CallStacks, CompiledContract, patch
from rift.core import (
    Entity,
    is_asm,
    is_impure,
    is_inline,
    is_inline_ref,
    is_method,
    is_method_id,
)
from rift.core.factory import Factory
from rift.core.utils import init_abstract_type
from rift.cst.cst_patcher import patch as cst_patch
from rift.cst.cst_visitor import relative_imports
from rift.func.util import cls_attrs
from rift.types import helpers


class Engine(object):
    """Engine responsible for compiling contracts."""

    VERBOSE = 0
    _cache = {}

    @classmethod
    def handle_docs(cls, contract, doc_string: str):
        if doc_string is None or doc_string.lstrip() == "":
            return
        d = textwrap.dedent(doc_string)
        lines = d.splitlines()
        idx = lines.index("# config") if "# config" in lines else -1
        if idx != -1:
            config_lines = lines[idx + 1 :]
            cfg = yaml.safe_load("\n".join(config_lines))
            cls.handle_config(contract, cfg)

    @classmethod
    def handle_config(cls, contract, cfg):
        for data_name in cfg["get-methods"]:
            model = contract.data
            annots = {
                "return": model.annotations[data_name],
            }
            annots["_method"] = {
                "impure": False,
                "inline": False,
                "inline_ref": False,
                "method_id": True,
                "method_id_v": None,
            }
            name = f"get_{data_name}"
            CallStacks.declare_method(
                name,
                [],
                annots,
            )
            r = model.get(data_name)
            helpers.ret_(r)
            CallStacks.end_method(name)

    @classmethod
    def compile(cls, contract):
        inst = contract()
        CallStacks.declare_contract(contract.__name__)
        setattr(inst, "__intercepted__", True)
        attrs = cls_attrs(contract)
        d = zip(attrs, [getattr(contract, attr) for attr in attrs])
        for name, value in d:
            if name == "__annotations__":
                # TODO: Handle global and state variables
                pass
            elif is_method(value):
                func_args = value.__args__
                names = list(value.__names__)
                annots = value.__annotations__
                annots = annots if annots else {}
                if "return" not in annots:
                    annots["return"] = None
                # TODO
                # Here we should check if any of args are Payload type
                # Why? -> To detect them and pass the slice instead
                # Also -> defined type should be slice
                data_classes = []
                for k, cls_ in list(annots.items()):
                    if (
                        hasattr(cls_, "__magic__")
                        and cls_.__magic__ == 0xA935E5
                    ):
                        annots.pop(k)
                        idx = names.index(k)
                        names[idx] = k + "_data"
                        annots[k + "_data"] = Factory.engines["Slice"]
                        data_classes.append((idx - 1, k + "_data", cls_))
                args = [
                    init_abstract_type(annots.get(arg, Entity), name=arg)
                    for arg in names[1:]
                ]
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
                # here we gather _data args and reconstruct class from them
                for _idx, _data, _cls in data_classes:
                    d = _cls(data_slice=args[_idx])
                    args[_idx] = d
                if not value.__static__:
                    inst.__refresh__(reset=True)
                    args = (inst, *args)
                else:
                    contract.__refresh__(contract, reset=True)
                    args = (contract, *args)
                res = value(*args, NO_INTERCEPT=1)
                if res == contract.NOT_IMPLEMENTED:
                    CallStacks.hide_method(name)
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
                if not asm_annots["hide"]:
                    CallStacks.declare_asm(
                        name,
                        [names[i + 1] for i in range(func_args - 1)],
                        annots,
                        asm_annots,
                    )
                    value(inst, *args, NO_INTERCEPT=1)
                    CallStacks.end_method(name)
            elif name == "__doc__":
                cls.handle_docs(contract, value)

        contract_ = CallStacks.get_contract(contract.__name__)
        return CompiledContract(contract_)

    @staticmethod
    def cst_patch(src):
        src = "from rift.types import helpers\n" + src
        src = cst_patch(src)
        return src

    @staticmethod
    def patch(contract, _globals, src_callback=None):
        lines, starting = inspect.findsource(contract)
        selected = lines[:starting]
        selected.insert(0, "from rift.types import helpers\n")
        needed_src = "".join(selected)
        needed_src = cst_patch(needed_src)
        rel_imported = relative_imports(needed_src)._imported_ones
        x = ast.parse(needed_src)
        m = {**_globals}
        exec(compile(x, "func-imports", "exec"), m)
        # here we will need to select updated contracts from _globals
        _selected = {k: v for k, v in _globals.items() if k in rel_imported}
        m = {**m, **_selected}
        src = inspect.getsource(contract)
        activate_func_mode = (
            "from rift.runtime.config import FunCMode\nFunCMode.activate()\n"
        )
        src = activate_func_mode + src
        src = cst_patch(src)
        x = ast.parse(src)
        patched_ast = patch(x)
        if src_callback:
            src_callback(patched_ast)
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
