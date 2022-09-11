from rift.ast.printer import Printer


class CompiledContract(object):
    """Instance of compiled contract."""

    def __init__(self, contract_ast):
        self.ast = contract_ast

    def to_func(self):
        printer = Printer()
        self.ast.print_func(printer)
        return printer.out()
