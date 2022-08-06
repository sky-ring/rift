from dbuilder.ast.printer import Printer
from dbuilder.ast.types.node import Node
from dbuilder.ast.utils import _type_name


class Statement(Node):
    RETURN = 0
    METHOD_CALL = 1
    FUNC_CALL = 2
    CONTROL_FLOW = 3
    EXPR = 4
    ASSIGN = 5
    M_ASSIGN = 6

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
                return '"%s"' % x
            return str(x)

        if self.type == Statement.FUNC_CALL:
            printer.print(
                "{op}{name}({args});",
                op="~" if self.args[0].endswith("_") else "",
                name=self.args[0].removesuffix("_"),
                args=",".join([transform(x) for x in self.args[1]]),
            )
        elif self.type == Statement.RETURN:
            obj = self.args[0]
            if obj is None:
                obj = "()"
            printer.print("return {object};", object=obj)
        elif self.type == Statement.METHOD_CALL:
            printer.print(
                "{object}{op}{name}({args});",
                op="~" if self.args[0].endswith("_") else ".",
                object=self.args[1],
                name=self.args[0].removesuffix("_"),
                args=",".join([transform(x) for x in self.args[2]]),
            )
        elif self.type == Statement.EXPR:
            expr = self.args[0]
            if not (hasattr(expr, "__hide__") and expr.__hide__):
                printer.print("{expr};", expr=expr)
        elif self.type == Statement.ASSIGN:
            expr = self.args[1]
            annotations = getattr(expr, "annotations")
            if annotations:
                type_hint = annotations["return"]
                type_hint = _type_name(type_hint)
            else:
                type_hint = "var"
            printer.print(
                "{type_} {v} = {expr};",
                type_=type_hint,
                v=self.args[0],
                expr=expr,
            )
        elif self.type == Statement.M_ASSIGN:
            v_list = self.args[0]
            expr = self.args[1]
            annotations = expr.annotations or {}
            ret_type = annotations.get("return")
            args = getattr(ret_type, "__args__", None)
            if args is None:
                args = ["var" for _ in v_list]
            if len(args) != len(v_list):
                raise RuntimeError("non matching outputs")
            t_decl = [
                "{type_} {v}".format(type_=_type_name(t), v=v)
                for v, t in zip(v_list, args)
            ]
            printer.print(
                "({t_decl}) = {expr};",
                t_decl=", ".join(t_decl),
                expr=expr,
            )
