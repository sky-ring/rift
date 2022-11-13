import libcst as cst


class GeneralImportVisitor(cst.CSTVisitor):
    _relative_accesses = []
    _imported_ones = []

    def __init__(self, target_module: str):
        self.target_module = target_module
        self.imports = {}

    def visit_ImportFrom(self, node: "cst.ImportFrom"):
        m = node.module
        if isinstance(m, cst.Attribute):
            if (
                isinstance(m.value, cst.Name)
                and m.value.value == self.target_module
            ):
                # Here we captured an `from [Target].[X] import [Names]`
                from_ = m.attr.value
                names = node.names
                if isinstance(names, cst.ImportStar):
                    # TODO: Disallow this explicitly
                    pass
                else:
                    names = [name.name.value for name in names]
                    self.imports[from_] = names
        return super().visit_ImportFrom(node)


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
            self._relative_accesses.append(m_name)
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
