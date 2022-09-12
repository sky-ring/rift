from rift.ast.calls import CallStacks
from rift.core.entity import mark
from rift.meta.utils import caller_locals


class While:
    def __init__(self, cond):
        self.cond = cond

    def __enter__(self):
        ctx = caller_locals(back=2)
        if "ctx" in ctx and hasattr(ctx["ctx"], "__refresh__"):
            ctx["ctx"].__refresh__()
        mark(self.cond)
        self.id = CallStacks.begin_while(self.cond)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        CallStacks.end_while(self.id)


def while_(cond):
    return While(cond)
