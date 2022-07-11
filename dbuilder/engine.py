import ast
import inspect

from dbuilder.annots import is_method
from dbuilder.calls import CallStacks
from dbuilder.entity import Entity
from dbuilder.magic import patch


class Engine(object):
    @staticmethod
    def compile(contract):
        inst = contract()
        CallStacks.declare_contract(contract.__name__)
        setattr(inst, "__intercepted__", True)
        for k in contract.__dict__:
            v = contract.__dict__[k]
            if k == "__annotations__":
                # for ak in v:
                #     atype = v[ak]
                #     if issubclass(atype, _FunCType):
                #         print("Detected state variable: ", ak, "->", atype)
                pass
            if is_method(v):
                l = v.__args__
                args = (Entity({"i": i}, name=v.__names__[i + 1]) for i in range(l - 1))
                CallStacks.declare_method(k, [v.__names__[i + 1] for i in range(l - 1)])
                r = v(inst, *args, NO_INTERCEPT=1)
                if isinstance(r, Entity):
                    CallStacks.return_(r)
                CallStacks.end_method(k)
        pass

    @staticmethod
    def patch(contract, _globals):
        src = inspect.getsource(contract)
        print(src)
        x = ast.parse(src)
        patched_ast = patch(x)
        m = {**_globals}
        exec(compile(patched_ast, "some-shit", "exec"), m)
        return m[contract.__name__]
