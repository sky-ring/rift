from dbuilder.ast.calls import CallStacks
from dbuilder.core.entity import mark


class While:
    def __init__(self, cond):
        self.cond = cond

    def __enter__(self):
        mark(self.cond)
        self.id = CallStacks.begin_while(self.cond)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        CallStacks.end_while(self.id)


def while_(cond):
    return While(cond)
