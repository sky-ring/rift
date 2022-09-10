import libcst as cst


class RelativeImportVisitor(cst.CSTVisitor):
    _relative_accesses = []
    _imported_ones = []

    def __init__(self):
        self._relative_accesses = []
        self._imported_ones = []
        self._detailed_imports = {}

    def visit_ImportFrom(self, node: "cst.ImportFrom"):
        if len(node.relative) == 1:
            m_name = node.module.value
            self._relative_accesses.append(node.module.value)
            if m_name not in self._detailed_imports:
                self._detailed_imports[m_name] = []
            imported = node.names
            if isinstance(imported, cst.ImportStar):
                # TODO: A good practice would be throwing
                # and disallowing relative * imports
                pass
            else:
                # TODO: A better practice would be capturing the aliases too
                for i in imported:
                    n = i.name.value
                    self._imported_ones.append(n)
                    self._detailed_imports[m_name].append(n)
        return super().visit_ImportFrom(node)
