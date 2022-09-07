import libcst as cst


class HexTransformer(cst.CSTTransformer):
    def leave_Integer(
        self,
        original_node: "cst.Integer",
        updated_node: "cst.Integer",
    ) -> "cst.BaseExpression":
        if updated_node.value.startswith("0x"):
            # detected hex constant
            new_node = cst.Call(
                cst.Attribute(cst.Name("helpers"), cst.Name("hex_int")),
                args=[cst.Arg(cst.SimpleString(f'"{updated_node.value}"'))],
            )
            return new_node
        return super().leave_Integer(original_node, updated_node)
