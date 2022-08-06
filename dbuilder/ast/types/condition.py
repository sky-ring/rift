from dbuilder.ast.printer import Printer
from dbuilder.ast.types.control_flow import ControlFlow
from dbuilder.ast.types.statement import Statement


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

    def add_statement(self, statement):
        self.states[self.current_cond].append(statement)

    def print_func(self, printer: Printer):
        class IfNode:
            def __init__(self, c, next):
                self.c = c
                self.next = next

        def print_if(node):
            c = node.c
            if c != "def":
                printer.print(
                    "if ({cond}) {{",
                    cond=self.cond_items[c] if c != "def" else "",
                )
                printer.incr_indent()
                for s in self.states[c]:
                    s.print_func(printer)
                printer.decr_indent()
                printer.print("}}")
                if node.next is not None:
                    printer.print("else {{")
                    printer.incr_indent()
                    print_if(node.next)
                    printer.decr_indent()
                    printer.print("}}")
            else:
                for s in self.states[c]:
                    s.print_func(printer)

        r = None
        for i in range(len(self.conds) - 1, -1, -1):
            n = IfNode(self.conds[i], r)
            r = n
        print_if(r)
