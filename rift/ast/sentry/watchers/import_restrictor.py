from typing import Any

from rift.ast.sentry.base_types import SentryEntry, SentryState
from rift.ast.sentry.watchers.codes import ErrorCode
from rift.ast.sentry.watchers.src_watcher import SrcWatcher
from rift.cst.cst_visitor import relative_imports, target_imports


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
        gi = target_imports(src, target=None)
        imports, loc_meta = gi.imports, gi.loc
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
