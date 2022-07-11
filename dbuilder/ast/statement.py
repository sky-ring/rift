from dbuilder.ast.node import Node
from dbuilder.ast.printer import Printer


class Statement(Node):
    RETURN = 0
    METHOD_CALL = 1
    FUNC_CALL = 2
    CONTROL_FLOW = 3
    EXPR = 4
    ASSIGN = 5

    def __init__(self, type, args):
        super().__init__()
        self.type = type
        self.args = args

    def add_statement(self, statement):
        pass

    def activates(self):
        return False

    def print_func(self, printer: Printer):
        def transform(x):
            if isinstance(x, str):
                return "\"%s\"" % x
            return str(x)
        if self.type == Statement.FUNC_CALL:
            printer.print(
                "{op}{name}({args});",
                op="~" if self.args[0].endswith("_") else "",
                name=self.args[0].removesuffix("_"),
                args=",".join(
                    [transform(x) for x in self.args[1]]
                )
            )
            pass
        elif self.type == Statement.RETURN:
            printer.print(
                "return {object};",
                object=self.args[0]
            )

            pass
        elif self.type == Statement.METHOD_CALL:
            printer.print(
                "{object}{op}{name}({args});",
                op="~" if self.args[0].endswith("_") else ".",
                object=self.args[1],
                name=self.args[0].removesuffix("_"),
                args=",".join(
                    [transform(x) for x in self.args[2]]
                )
            )
            pass
        elif self.type == Statement.EXPR:
            printer.print(
                "{expr};",
                expr=self.args[0]
            )
        elif self.type == Statement.ASSIGN:
            printer.print(
                "{v} = {expr};",
                v=self.args[0],
                expr=self.args[1]
            )
