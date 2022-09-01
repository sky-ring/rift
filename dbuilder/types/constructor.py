from dbuilder.core import Entity
from dbuilder.core.condition import Cond
from dbuilder.library.std import std
from dbuilder.types.bases.entity_base import _EntityBase
from dbuilder.types.types import Builder, Slice


class ConstructorType(_EntityBase):
    which: Entity
    bound: Entity

    def __getattr__(self, item):
        return getattr(self.bound, item)

    @classmethod
    def __serialize__(
        cls,
        to: "Builder",
        value: "ConstructorType",
    ) -> "Builder":
        # TODO : Completion
        return to

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
    ):
        bases = cls.__x_bases__
        m = ConstructorType()
        tag = std.null()
        tag.__assign__(f"{name}_tag")
        with Cond() as c:
            for base in bases:
                tag_len, tag_ = base.tag_data()
                read_tag = from_.uint(tag_len)
                c.match(read_tag == tag_)
                n_tag = from_.uint_(tag_len)
                n_tag.__assign__(f"{name}_tag")
                d = base.__deserialize__(
                    from_,
                    name=name,
                    inplace=inplace,
                    tag=False,
                )
                m.bound = d
        m.which = tag
        return m

    @classmethod
    def __predefine__(
        cls,
        name: str = None,
    ):
        bases = cls.__x_bases__
        for base in bases:
            base.__predefine__(name=name)


class _ConstructorTypeBuilder(type):
    def __new__(cls, *bases):
        names = (base.__name__ for base in bases)
        joined = "_".join(names)
        return super().__new__(
            cls,
            "Constructor_%s" % joined,
            (ConstructorType,),
            {
                "__x_bases__": list(bases),
            },
        )


def Constructor(*bases):
    return _ConstructorTypeBuilder.__new__(_ConstructorTypeBuilder, *bases)
