from dbuilder.ast.node import Node
from dbuilder.ast.printer import Printer
from dbuilder.ast.statement import Statement


class Method(Node):
    statements: list[Statement] = []
    active_statement: list[Statement] = []

    def __init__(self, name, args):
        super().__init__()
        self.name = name
        self.args = args
        self.statements = []
        self.active_statement = []

    def add_statement(self, statement):
        if len(self.active_statement) > 0:
            active = self.active_statement[0]
            active.add_statement(statement)
            if statement.activates():
                self.active_statement.insert(0, statement)
        else:
            self.statements.append(statement)
            if statement.activates():
                self.active_statement.insert(0, statement)

    def end_statement(self, statement):
        self.active_statement.remove(statement)

    def print_func(self, printer: Printer):
        printer.print(
            "{output} {name}({args}) {{",
            output="_",
            name=self.name,
            args=", ".join(self.args),
            o="{"
        )
        printer.incr_indent()
        for s in self.statements:
            s.print_func(printer)
        printer.decr_indent()
        printer.print("}}")
