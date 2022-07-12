import ast
import inspect

from dbuilder.core import is_method, Entity
from dbuilder.func import CallStacks, patch, CompiledContract


class Engine(object):
    @staticmethod
    def compile(contract):
        inst = contract()
        CallStacks.declare_contract(contract.__name__)
        setattr(inst, "__intercepted__", True)
        for k in contract.__dict__:
            v = contract.__dict__[k]
            if k == "__annotations__":
                # TODO: Handle global and state variables
                pass
            if is_method(v):
                l = v.__args__
                args = (Entity({"i": i}, name=v.__names__[
                        i + 1]) for i in range(l - 1))
                CallStacks.declare_method(
                    k, [v.__names__[i + 1] for i in range(l - 1)])
                r = v(inst, *args, NO_INTERCEPT=1)
                if isinstance(r, Entity):
                    CallStacks.return_(r)
                CallStacks.end_method(k)
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
