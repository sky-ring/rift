from dbuilder.ast.calls import CallStacks
from dbuilder.core.entity import mark


class Cond:
    C_ID = 0

    def __init__(self):
        Cond.C_ID += 1
        self.id = Cond.C_ID
        self.index = 0
        self.conds = []

    def match(self, cond):
        mark(cond)
        self.index += 1
        self.conds.append(cond)
        if self.index == 1:
            self.id = CallStacks.begin_if(cond)
        else:
            CallStacks.else_if(self.id, cond)

    def otherwise(self):
        CallStacks.else_if(self.id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        CallStacks.end_if(self.id)
