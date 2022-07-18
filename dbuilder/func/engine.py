import ast
import inspect

from dbuilder.core import is_method, Entity
from dbuilder.core.utils import init_abstract_type
from dbuilder.func import CallStacks, patch, CompiledContract


class Engine(object):
    """Engine responsible for compiling contracts."""

    @staticmethod
    def compile(contract):
        inst = contract()
        inst.ret_ = (
            lambda *t: CallStacks.return_(*t)
            if len(t) != 0
            else CallStacks.return_(None)
        )
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
                e_annots = annots if annots else {}
                args = (
                    init_abstract_type(e_annots.get(arg, Entity), name=arg)
                    for arg in names[1:]
                )
                CallStacks.declare_method(
                    name,
                    [names[i + 1] for i in range(func_args - 1)],
                    annots,
                )
                value(inst, *args, NO_INTERCEPT=1)
                CallStacks.end_method(name)
        contract_ = CallStacks.get_contract(contract.__name__)
        return CompiledContract(contract_)

    @staticmethod
    def patch(contract, _globals):
        src = inspect.getsource(contract)
        print(src)
        x = ast.parse(src)
        patched_ast = patch(x)
        y = ast.unparse(patched_ast)
        print(y)
        m = {**_globals}
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
        t_globals["Engine"].patched = lambda c: c
        patched = Engine.patch(contract, t_globals)
        patched.__is_patched__ = True
        return patched
