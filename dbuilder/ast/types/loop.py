from dbuilder.ast.printer import Printer
from dbuilder.ast.types.block import Block
from dbuilder.ast.types.control_flow import ControlFlow


class WhileLoop(ControlFlow):
    states: Block

    def __init__(self, cond):
        super().__init__()
        self.cond = cond
        self.states = None

    def add_statement(self, statement):
        if not self.states:
            self.states = self._new_block()
        self.states.add_statement(statement)

    def print_func(self, printer: Printer):
        printer.print(
            "while ({cond}) {{",
            cond=self.cond,
        )
        printer.incr_indent()
        self.states.print_func(printer)
        printer.decr_indent()
        printer.print("}}")
