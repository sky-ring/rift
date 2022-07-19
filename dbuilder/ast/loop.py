from dbuilder.ast import ControlFlow, Printer, Statement


class WhileLoop(ControlFlow):
    states: list[Statement]

    def __init__(self, cond):
        super().__init__()
        self.cond = cond
        self.states = []

    def add_statement(self, statement):
        self.states.append(statement)

    def print_func(self, printer: Printer):
        printer.print(
            "while ({cond}) {{",
            cond=self.cond,
        )
        printer.incr_indent()
        for s in self.states:
            s.print_func(printer)
        printer.decr_indent()
        printer.print("}}")
