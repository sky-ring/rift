from rift.ast.calls import CallStacks
from rift.core.entity import mark
from rift.core.utils import refresh_context, restrain_context
from rift.meta.utils import caller_locals


class Cond:
    C_ID = 0

    def __init__(self):
        Cond.C_ID += 1
        self.id = Cond.C_ID
        self.index = 0
        self.conds = []

    def match(self, cond):
        ctx = caller_locals(back=2)
        if self.index != 0:
            # release the previous guy
            restrain_context(ctx)
        refresh_context(ctx)
        mark(cond)
        self.index += 1
        self.conds.append(cond)
        if self.index == 1:
            self.id = CallStacks.begin_if(cond)
        else:
            CallStacks.else_if(self.id, cond)

    def otherwise(self):
        ctx = caller_locals(back=2)
        if self.index != 0:
            # release the previous guy
            restrain_context(ctx)
        refresh_context(ctx)
        CallStacks.else_if(self.id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ctx = caller_locals(back=2)
        restrain_context(ctx)
        CallStacks.end_if(self.id)
