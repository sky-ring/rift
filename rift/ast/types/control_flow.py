from rift.ast.types.block import Block
from rift.ast.types.statement import Statement


class ControlFlow(Statement):
    def __init__(self):
        super().__init__(Statement.CONTROL_FLOW, ())

    def activates(self):
        return True

    def _new_block(self):
        b = Block()
        b.parent = self.parent
        return b
