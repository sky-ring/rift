from rift.ast.printer import Printer
from rift.ast.types.node import Node
from rift.ast.types.statement import Statement
from rift.ast.utils import _type_name


class AsmMethod(Node):
    statement: Statement

    def __init__(self, name, args, annotations, asm_annotations):
        super().__init__()
        self.name = name
        self.args = args
        self.annotations = annotations
        self.asm_annotations = asm_annotations
        self.statement = None

    def add_statement(self, statement):
        if statement.type != Statement.RETURN:
            raise RuntimeError("Unexpected statement on asm method")
        self.statement = statement

    def _get_specs(self):
        sd = self.annotations.get("_method")
        if not sd:
            return ""
        res = []
        if sd["impure"]:
            res.append("impure")
        if sd["inline"]:
            res.append("inline")
        elif sd["inline_ref"]:
            res.append("inline_ref")
        elif sd["method_id"]:
            if sd["method_id_v"]:
                res.append("method_id(%d)" % sd["method_id_v"])
            else:
                res.append("method_id")
        if len(res) == 0:
            return ""
        return " ".join(res) + " "

    def print_func(self, printer: Printer):
        type_namer = lambda x: "{type} {name}".format(
            type=_type_name(x[0]),
            name=x[1],
        )
        tupler = lambda x: (self.annotations[x], x)
        arg_defs = list(map(type_namer, map(tupler, self.args)))

        name = self.name
        fname = self.annotations["_fname"]
        name = name if fname is None else fname

        entity = self.statement.args[0]
        entity = entity if isinstance(entity, tuple) else (entity,)
        rearrange = []
        input_order = self.asm_annotations["input_order"]
        out_order = self.asm_annotations["out_order"]
        # TODO: Check Args (Better on annotation side)
        if input_order:
            input_arrange = " ".join(input_order)
            rearrange.append(input_arrange)
        if out_order:
            out_arrange = "-> " + " ".join(str(i) for i in out_order)
            rearrange.append(out_arrange)
        rearrange = " ".join(rearrange)
        if rearrange != "":
            rearrange = f"({rearrange})"

        printer.print(
            "{output} {name}({args}) {specs}asm{rearrange} {entity};",
            output=_type_name(self.annotations["return"]),
            name=name,
            args=", ".join(arg_defs),
            specs=self._get_specs(),
            o="{",
            rearrange=rearrange,
            entity=" ".join(f'"{x}"' for x in entity),
        )
