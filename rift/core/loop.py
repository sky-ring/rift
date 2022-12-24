from rift.ast.calls import CallStacks
from rift.core.entity import mark
from rift.core.utils import refresh_context, restrain_context
from rift.meta.utils import caller_locals


class While:
    def __init__(self, cond):
        self.cond = cond

    def __enter__(self):
        ctx = caller_locals(back=2)
        refresh_context(ctx)
        mark(self.cond)
        self.id = CallStacks.begin_while(self.cond)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ctx = caller_locals(back=2)
        restrain_context(ctx)
        CallStacks.end_while(self.id)


def while_(cond):
    return While(cond)
