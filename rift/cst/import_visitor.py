import libcst as cst


class GeneralImportVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def __init__(self, target_module: str = None):
        super().__init__()
        self.target_module = target_module
        self.global_ = self.target_module is None
        self.imports = {}
        self.loc = {}

    def visit_ImportFrom(self, node: "cst.ImportFrom"):
        pos = self.get_metadata(cst.metadata.PositionProvider, node).start
        if len(node.relative) != 0:
            return super().visit_ImportFrom(node)
        m = node.module
        if isinstance(m, cst.Attribute) or isinstance(m, cst.Name):
            name = parse_name(m)
            r_tg = name.split(".")[0]
            if r_tg == self.target_module or self.global_:
                # Captured expression: from [Target](.[X])* import [Names]
                if not self.global_:
                    name = name.removeprefix(r_tg + ".")
                names = node.names
                if isinstance(names, cst.ImportStar):
                    self.imports[name] = ["*"]
                else:
                    names = [name.name.value for name in names]
                    self.imports[name] = names
                self.loc[name] = (pos.line - 1, pos.column)
        else:
            raise RuntimeError("Unsupported Import Expression!")
        return super().visit_ImportFrom(node)


class RelativeImportVisitor(cst.CSTVisitor):
    _relative_accesses = []
    _imported_ones = []

    def __init__(self):
        super().__init__()
        self._relative_accesses = []
        self._imported_ones = []
        self.imports = {}

    def visit_ImportFrom(self, node: "cst.ImportFrom"):
        if len(node.relative) == 1:
            m_name = node.module.value
            self._relative_accesses.append(m_name)
            if m_name not in self.imports:
                self.imports[m_name] = []
            imported = node.names
            if isinstance(imported, cst.ImportStar):
                # TODO: A good practice would be throwing
                # and disallowing relative * imports
                self.imports[m_name].append("*")
                pass
            else:
                # TODO: A better practice would be capturing the aliases too
                for i in imported:
                    n = i.name.value
                    self._imported_ones.append(n)
                    self.imports[m_name].append(n)
        elif len(node.relative) > 1:
            raise RuntimeError("Unsupported Import Expression!")
        return super().visit_ImportFrom(node)


class ModuleImportVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.PositionProvider,)

    def __init__(self):
        super().__init__()
        self.imports = []
        self.loc = {}

    def visit_Import(self, node: "cst.Import"):
        pos = self.get_metadata(cst.metadata.PositionProvider, node).start
        for alias in node.names:
            name = parse_name(alias.name)
            self.imports.append(name)
            self.loc[name] = (pos.line - 1, pos.column)
        return super().visit_Import(node)


def parse_name(node: cst.Name | cst.Attribute) -> str:
    if isinstance(node, cst.Name):
        return node.value
    return parse_name(node.value) + "." + parse_name(node.attr)
