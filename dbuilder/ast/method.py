from dbuilder.ast import Node, Printer, Statement
from types import GenericAlias


class Method(Node):
    statements: list[Statement] = []
    active_statement: list[Statement] = []

    def __init__(self, name, args, annotations):
        super().__init__()
        self.name = name
        self.args = args
        self.annotations = annotations
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

    def _type_name(self, type_):
        if isinstance(type_, GenericAlias) and type_.__origin__ == tuple:
            types = map(self._type_name, type_.__args__)
            names = ", ".join(types)
            n = "({names})".format(names=names)
            return n
        elif hasattr(type_, "type_name"):
            return type_.type_name()
        elif type_ is None:
            return "()"
        elif type_ == int:
            return "int"
        return "_"

    def print_func(self, printer: Printer):
        type_namer = lambda x: "{type} {name}".format(
            type=self._type_name(x[0]), name=x[1]
        )
        tupler = lambda x: (self.annotations[x], x)
        arg_defs = list(map(type_namer, map(tupler, self.args)))
        printer.print(
            "{output} {name}({args}) {{",
            output=self._type_name(self.annotations["return"]),
            name=self.name,
            args=", ".join(arg_defs),
            o="{",
        )
        printer.incr_indent()
        for s in self.statements:
            s.print_func(printer)
        printer.decr_indent()
        printer.print("}}")
