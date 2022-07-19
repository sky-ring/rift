from types import GenericAlias

from dbuilder.core import Entity
from dbuilder.types.types import Tensor


def init_abstract_type(cls_, *args, **kwargs):
    filter_d = {int: Entity}
    cls_ = filter_d.get(cls_, cls_)
    if isinstance(cls_, GenericAlias) and cls_.__origin__ == tuple:
        t = Tensor(
            *args,
            [init_abstract_type(c) for c in cls_.__args__],
            **kwargs,
        )
        return t
    return cls_.abstract_init(*args, **kwargs)
