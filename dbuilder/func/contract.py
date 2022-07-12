from dbuilder import Printer


class CompiledContract:
    def __init__(self, contract_ast):
        self.ast = contract_ast

    def to_func(self):
        p = Printer()
        self.ast.print_func(p)
        return p.out()
