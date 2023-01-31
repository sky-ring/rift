from rift.ast.printer import Printer


class CompiledContract(object):
    """Instance of compiled contract."""

    def __init__(self, contract_ast):
        self.ast = contract_ast

    def to_func(self):
        printer = Printer()
        printer.print("const int False = 0;")
        printer.print("const int True = -1;")
        self.ast.print_func(printer)
        return printer.out()
