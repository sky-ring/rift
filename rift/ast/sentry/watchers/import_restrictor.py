from rift.ast.sentry.base_types import SentryEntry, SentryState
from rift.ast.sentry.watchers.codes import ErrorCode
from rift.ast.sentry.watchers.src_watcher import SrcWatcher
from rift.cst.cst_visitor import (
    relative_imports,
    target_imports,
    module_imports,
)


class ImportRestrictor(SrcWatcher):
    def __init__(
        self,
        name,
        code=ErrorCode.RestrictUnknown,
    ):
        self.name = name
        self.code = code

    def watch(self, src: str):
        _ = relative_imports(src)
        # TODO: is it good idea to restrict relative imports ?!
        mi = module_imports(src)
        imports_m, loc_meta_m = mi.imports, mi.loc
        gi = target_imports(src, target=None)
        imports, loc_meta = gi.imports, gi.loc
        # Logic's same -> Merge entries
        imports = {*imports.keys(), *imports_m}
        loc_meta = {**loc_meta, **loc_meta_m}
        imports = sorted(imports, key=lambda x: loc_meta[x])
        errs = []
        for k in imports:
            top = k.split(".")[0]
            if top != "rift":
                errs.append(
                    SentryEntry(
                        SentryState.HALT,
                        None,
                        loc_meta[k],
                        self.code,
                        f'Imports from non-rift modules are not supported: "{k}"',
                    ),
                )
        return errs, True
