from typing import TYPE_CHECKING

from rift.ast.bool_dict import BoolDict
from rift.ast.printer import Printer
from rift.ast.types.node import Node

if TYPE_CHECKING:
    from rift.ast.types.statement import Statement


class Block(Node):
    parent: "Block"
    symbols: BoolDict
    statements: list["Statement"]

    def __init__(self):
        super().__init__()
        self.parent = None
        self.symbols = BoolDict()
        # Just a simple patch to not define _ as a variable
        self.symbols["_"] = True
        self.statements = []

    def add_statement(self, statement):
        statement.parent = self
        self.statements.append(statement)
        statement.refresh()

    def _accessible(self, name):
        tg = self
        while tg is not None:
            if tg.symbols.has(name):
                return True
            else:
                tg = tg.parent
        return False

    def define(self, name):
        self.symbols[name] = True

    def print_func(self, printer: Printer):
        for s in self.statements:
            s.print_func(printer)
