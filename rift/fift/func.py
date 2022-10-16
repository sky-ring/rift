from tempfile import NamedTemporaryFile

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
            f = NamedTemporaryFile(
                prefix=f"source-{i}", suffix=".fc", mode="w", delete=False
            )
            f_sources.append(f.name)
            f.write(s)
            f.close()
        return cls.compile(*f_sources, optimization_level=optimization_level)
