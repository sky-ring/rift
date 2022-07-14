import ast
import inspect

from dbuilder.core import is_method, Entity
from dbuilder.func import CallStacks, patch, CompiledContract


class Engine(object):
    """Engine responsible for compiling contracts."""

    @staticmethod
    def compile(contract):
        inst = contract()
        CallStacks.declare_contract(contract.__name__)
        setattr(inst, "__intercepted__", True)
        for name, value in contract.__dict__.items():
            if name == "__annotations__":
                # TODO: Handle global and state variables
                pass
            if is_method(value):
                func_args = value.__args__
                names = value.__names__
                annots = value.__annotations__
                args = (
                    Entity({"i": i}, name=names[i + 1])
                    for i in range(func_args - 1)
                )
                CallStacks.declare_method(
                    name,
                    [names[i + 1] for i in range(func_args - 1)],
                    annots,
                )
                ret = value(inst, *args, NO_INTERCEPT=1)
                if isinstance(ret, Entity):
                    CallStacks.return_(ret)
                CallStacks.end_method(name)
        contract_ = CallStacks.get_contract(contract.__name__)
        return CompiledContract(contract_)

    @staticmethod
    def patch(contract, _globals):
        src = inspect.getsource(contract)
        print(src)
        x = ast.parse(src)
        patched_ast = patch(x)
        m = {**_globals}
        exec(compile(patched_ast, "func-patching", "exec"), m)
        return m[contract.__name__]
