from rift.ast.printer import Printer
from rift.ast.types.method import Method
from rift.ast.types.node import Node


class Contract(Node):
    methods: list[Method] = []
    hidden_methods: list[Method] = []
    vars = []
    current_method: Method = None

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.methods = []

    def add_method(self, method):
        self.current_method = method
        self.methods.append(method)

    def add_statement(self, statement):
        if not self.current_method:
            return
        self.current_method.add_statement(statement)

    def end_method(self, method):
        self.current_method = None

    def hide_method(self, method):
        tg = None
        tg_i = -1
        for i, m in enumerate(self.methods):
            if m.name == method:
                tg = m
                tg_i = i
        if tg is None:
            return
        self.methods.pop(tg_i)
        self.hidden_methods.append(tg)

    def add_variable(self):
        pass

    def print_func(self, printer: Printer):
        for m in self.methods:
            m.print_func(printer)
