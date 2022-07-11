from dbuilder.ast.statement import Statement


class ControlFlow(Statement):
    def __init__(self):
        super().__init__(Statement.CONTROL_FLOW, ())

    def activates(self):
        return True
