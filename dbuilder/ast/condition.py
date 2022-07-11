from dbuilder.ast.control_flow import ControlFlow
from dbuilder.ast.printer import Printer
from dbuilder.ast.statement import Statement


class IfFlow(ControlFlow):
    states: dict[str, list[Statement]]
    def __init__(self):
        super().__init__()
        self.conds = []
        self.cond_items = {}
        self.states = {"def": []}

    def iff(self, cond):
        self.conds.append(cond.node_id())
        self.cond_items[cond.node_id()] = cond
        self.current_cond = cond.node_id()
        self.states[self.current_cond] = []

    def else_(self):
        self.current_cond = "def"
        self.conds.append("def")
        self.states[self.current_cond] = []
        pass

    def add_statement(self, statement):
        self.states[self.current_cond].append(statement)
        pass

    def print_func(self, printer: Printer):
        for i, c in enumerate(self.conds):
            printer.print(
                "{kw} {_is}{cond}{_is_} {{",
                cond=self.cond_items[c] if c != "def" else "",
                kw="if" if i == 0 else "else",
                _is="(" if c != "def" else "",
                _is_=")" if c != "def" else "",
            )
            printer.incr_indent()
            for s in self.states[c]:
                s.print_func(printer)
            printer.decr_indent()
            printer.print("}}")


