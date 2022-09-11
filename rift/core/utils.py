from types import GenericAlias

from rift.core.factory import Factory


def init_abstract_type(cls_, *args, **kwargs):
    entity_cls = Factory.engines["Entity"]
    filter_d = {int: Factory.engines["Int"], None: entity_cls}
    cls_ = filter_d.get(cls_, cls_)
    if isinstance(cls_, str):
        if cls_ in Factory.engines:
            cls_ = Factory.engines[cls_]
        else:
            print("warning, dangling class: ", cls_)
    if isinstance(cls_, GenericAlias) and cls_.__origin__ == tuple:
        t = Factory.build(
            "Tensor",
            *args,
            [init_abstract_type(c) for c in cls_.__args__],
            type_=cls_,
            **kwargs,
        )
        return t
    return cls_.abstract_init(*args, **kwargs)
