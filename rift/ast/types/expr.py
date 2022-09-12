from rift.ast.ref_table import ReferenceTable


class Expr:
    EXPR_AR2 = 0
    EXPR_CALL = 1
    EXPR_FUNC = 2
    EXPR_AR1 = 3
    EXPR_VAR = 4
    EXPR_CONST = 5

    def __init__(self, type, *args, annotations=None):
        self.type = type
        self.args = args
        self.annotations = annotations
        if self.annotations:
            self.annotations = {**self.annotations}

    @staticmethod
    def call_expr(operand, method, *args, annotations=None):
        ReferenceTable.mark(operand, *args)
        e = Expr(
            Expr.EXPR_CALL,
            operand,
            method,
            *args,
            annotations=annotations,
        )
        return e

    @staticmethod
    def call_func(method, *args, annotations=None):
        ReferenceTable.mark(*args)
        e = Expr(Expr.EXPR_FUNC, method, *args, annotations=annotations)
        return e

    @staticmethod
    def binary_op(op, op1, op2, type_):
        ReferenceTable.mark(op1, op2)
        e = Expr(Expr.EXPR_AR2, op, op1, op2, annotations={"return": type_})
        return e

    @staticmethod
    def unary_op(op, operand, type_):
        ReferenceTable.mark(operand)
        e = Expr(Expr.EXPR_AR1, op, operand, annotations={"return": type_})
        return e

    @staticmethod
    def variable(x, type_=None):
        ReferenceTable.ref(x)
        e = Expr(Expr.EXPR_VAR, x, annotations={"return": type_})
        return e

    @staticmethod
    def const(x):
        ReferenceTable.mark(x)
        e = Expr(Expr.EXPR_CONST, x)
        if isinstance(x, int):
            e.annotations = {"return": int}
        return e

    def __repr__(self):
        def transform(x):
            if isinstance(x, str):
                return '"%s"' % x
            return str(x)

        if self.type == Expr.EXPR_AR2:
            op = self.args[0]
            wrap = False
            if op == "&" or op == "|":
                wrap = True
            return "{wrap_s}{op1}{wrap_e} {op} {wrap_s}{op2}{wrap_e}".format(
                op1=self.args[1],
                op=self.args[0],
                op2=self.args[2],
                wrap_s="(" if wrap else "",
                wrap_e=")" if wrap else "",
            )
        elif self.type == Expr.EXPR_AR1:
            return "{op} {ope}".format(op=self.args[0], ope=self.args[1])
        elif self.type == Expr.EXPR_CALL:
            return "{object}{op}{name}({args})".format(
                op="~" if self.args[1].endswith("_") else ".",
                object=self.args[0],
                name=self.args[1].removesuffix("_"),
                args=", ".join([transform(x) for x in self.args[2:]]),
            )
        elif self.type == Expr.EXPR_FUNC:
            return "{op}{name}({args})".format(
                op="~" if self.args[0].endswith("_") else "",
                name=self.args[0].removesuffix("_"),
                args=", ".join([transform(x) for x in self.args[1:]]),
            )
        elif self.type == Expr.EXPR_VAR:
            return "{name}".format(name=self.args[0])
        elif self.type == Expr.EXPR_CONST:
            return "{value}".format(value=repr(self.args[0]))
