from dbuilder.ast.types.block import Block
from dbuilder.ast.types.statement import Statement


class ControlFlow(Statement):
    def __init__(self):
        super().__init__(Statement.CONTROL_FLOW, ())

    def activates(self):
        return True

    def _new_block(self):
        b = Block()
        b.parent = self.parent
        return b
