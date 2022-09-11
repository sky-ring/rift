from rift.ast.printer import Printer
from rift.ast.types.block import Block
from rift.ast.types.control_flow import ControlFlow
from rift.ast.types.statement import Statement


class IfFlow(ControlFlow):
    states: dict[str, Block]

    def __init__(self):
        super().__init__()
        self.conds = []
        self.cond_items = {}
        self.states = {"def": self._new_block()}

    def iff(self, cond):
        self.conds.append(cond.node_id())
        self.cond_items[cond.node_id()] = cond
        self.current_cond = cond.node_id()
        self.states[self.current_cond] = self._new_block()

    def else_(self):
        self.current_cond = "def"
        self.conds.append("def")
        self.states[self.current_cond] = self._new_block()

    def add_statement(self, statement):
        self.states[self.current_cond].add_statement(statement)

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
                self.states[c].print_func(printer)
                printer.decr_indent()
                printer.print("}}")
                if node.next is not None:
                    printer.print("else {{")
                    printer.incr_indent()
                    print_if(node.next)
                    printer.decr_indent()
                    printer.print("}}")
            else:
                self.states[c].print_func(printer)

        r = None
        for i in range(len(self.conds) - 1, -1, -1):
            n = IfNode(self.conds[i], r)
            r = n
        print_if(r)
