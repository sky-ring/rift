import libcst as cst


class RelativeImportVisitor(cst.CSTVisitor):
    _relative_accesses = []

    def __init__(self):
        self._relative_accesses = []

    def visit_ImportFrom(self, node: "cst.ImportFrom"):
        if len(node.relative) == 1:
            self._relative_accesses.append(node.module.value)
        return super().visit_ImportFrom(node)
