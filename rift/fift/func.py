import base64
import zlib
from tempfile import NamedTemporaryFile

from rift.fift.bundled_fc import FUNC_LIBS
from rift.fift.fift import Fift


class FunCResult:
    fift_code: str


class FunCError:
    error: str

    def __repr__(self) -> str:
        return f"FunCError{{\n\t{self.error}\n}}"


class FunCConfig:
    optimization_level: int = 2
    sources: list[str] = []

    def __entry__(self) -> dict:
        return {
            "optLevel": self.optimization_level,
            "sources": self.sources,
        }


class FunC:
    @classmethod
    def compile(cls, *files, optimization_level=2):
        config = FunCConfig()
        config.optimization_level = optimization_level
        config.sources = list(files)
        res = Fift.func_compile(config.__entry__())
        if res["status"] == "ok":
            r = FunCResult()
            r.fift_code = res["fiftCode"]
            r.fift_code = r.fift_code.replace("\\n", "\n")
            return r
        elif res["status"] == "error":
            e = FunCError()
            e.error = res["message"]
            return e
        else:
            raise RuntimeError("Unexpected result: ", res)

    @classmethod
    def compile_source(cls, *sources, optimization_level=2):
        f_sources = []
        for i, s in enumerate(sources):
            if s.startswith("#"):
                # We load the libraries dude
                i = s.replace("#", "").strip()
                code = FUNC_LIBS[i]
                zc = base64.b64decode(code)
                s = zlib.decompress(zc).decode("utf-8")
            f = NamedTemporaryFile(
                prefix=f"source-{i}-",
                suffix=".fc",
                mode="w",
                delete=False,
                encoding="utf-8",
            )
            f_sources.append(f.name)
            f.write(s)
            f.close()
        return cls.compile(*f_sources, optimization_level=optimization_level)

    @classmethod
    def compile_link(cls, files, links, optimization_level=2):
        f_sources = []
        for i, s in enumerate(links):
            if s.startswith("#"):
                # We load the libraries dude
                i = s.replace("#", "").strip()
                code = FUNC_LIBS[i]
                zc = base64.b64decode(code)
                s = zlib.decompress(zc).decode("utf-8")
            else:
                raise RuntimeError("Unknown library")
            f = NamedTemporaryFile(
                prefix=f"source-{i}-",
                suffix=".fc",
                mode="w",
                delete=False,
                encoding="utf-8",
            )
            f_sources.append(f.name)
            f.write(s)
            f.close()
        f_sources.extend(files)
        return cls.compile(*f_sources, optimization_level=optimization_level)
