from dbuilder.ast.types import Expr
from dbuilder.core import Entity
from dbuilder.core.factory import Factory
from dbuilder.core.invokable import typed_invokable


class Int(Entity):
    def __init__(self, value, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        self.data = Expr.const(value)

    @classmethod
    def abstract_init(cls, *args, **kwargs) -> "Int":
        return cls(0, *args, **kwargs)

    @classmethod
    def type_name(cls) -> str:
        return "int"

    def _repr_(self):
        return str(self.value)


class Slice(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "slice"

    @typed_invokable(name="load_coins_", return_=Int)
    def coin(self) -> int:
        pass

    @typed_invokable(name="load_uint_")
    def uint_(self, bits: int) -> int:
        pass

    @typed_invokable(name="preload_uint")
    def uint(self, bits: int) -> int:
        pass

    @typed_invokable(name="load_int_")
    def int_(self, bits: int) -> int:
        pass

    @typed_invokable(name="preload_int")
    def int(self, bits: int) -> int:
        pass

    @typed_invokable(name="slice_hash")
    def hash(self) -> int:
        pass

    @typed_invokable(name="string_hash")
    def string_hash(self) -> int:
        pass

    @typed_invokable(name="check_data_signature")
    def check_signature(self, signature: "Slice", public_key: int) -> int:
        pass

    @typed_invokable(name="slice_compute_data_size")
    def compute_data_size(self, max_cells: int) -> tuple[int, int, int]:
        pass

    @typed_invokable(name="bless")
    def bless(self) -> "Cont":
        pass

    @typed_invokable(name="end_parse")
    def end_parse(self) -> None:
        pass

    @typed_invokable(name="load_ref")
    def ref_(self) -> "Cell":
        pass

    @typed_invokable(name="preload_ref")
    def ref(self) -> "Cell":
        pass

    @typed_invokable(name="load_bits")
    def bits_(self, len_: int) -> "Slice":
        pass

    @typed_invokable(name="preload_bits")
    def bits(self, len_: int) -> "Slice":
        pass

    @typed_invokable(name="skip_bits")
    def skip_n(self, len_: int) -> None:
        pass

    @typed_invokable(name="skip_bits")
    def skip_n_(self, len_: int) -> None:
        pass

    @typed_invokable(name="first_bits")
    def first_bits(self, len_: int) -> "Slice":
        pass

    @typed_invokable(name="skip_last_bits")
    def skip_last_n(self, len_: int) -> None:
        pass

    @typed_invokable(name="skip_last_bits")
    def skip_last_n_(self, len_: int) -> None:
        pass

    @typed_invokable(name="slice_last")
    def slice_last(self, len_: int) -> "Slice":
        pass

    @typed_invokable(name="load_dict")
    def ldict_(self) -> "Cell":
        pass

    @typed_invokable(name="preload_dict")
    def ldict(self) -> "Cell":
        pass

    @typed_invokable(name="skip_dict")
    def skip_dict(self) -> None:
        pass

    @typed_invokable(name="load_maybe_ref")
    def maybe_ref_(self) -> "Cell":
        pass

    @typed_invokable(name="preload_maybe_ref")
    def maybe_ref(self) -> "Cell":
        pass

    @typed_invokable(name="slice_refs")
    def refs_n(self) -> int:
        pass

    @typed_invokable(name="slice_bits")
    def bits_n(self) -> int:
        pass

    @typed_invokable(name="slice_bits_refs")
    def bits_refs_n(self) -> tuple[int, int]:
        pass

    @typed_invokable(name="slice_empty?")
    def is_empty(self) -> int:
        pass

    @typed_invokable(name="slice_data_empty?")
    def is_data_empty(self) -> int:
        pass

    @typed_invokable(name="slice_refs_empty?")
    def are_refs_empty(self) -> int:
        pass

    @typed_invokable(name="slice_depth")
    def depth(self) -> int:
        pass

    @typed_invokable(name="load_msg_addr")
    def addr_(self) -> "Slice":
        pass

    @typed_invokable(name="parse_addr")
    def parse_addr(self) -> "Tuple":
        pass

    @typed_invokable(name="parse_std_addr")
    def parse_std_addr(self) -> tuple[int, int]:
        pass

    @typed_invokable(name="parse_var_addr")
    def parse_var_addr(self) -> tuple[int, "Slice"]:
        pass

    @typed_invokable(name="equal_slices")
    def is_equal(self, b: "Slice") -> int:
        pass


class Cont(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "cont"


class String(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "string"


class Cell(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "cell"

    @typed_invokable(name="begin_parse")
    def parse(self) -> Slice:
        pass

    @typed_invokable(name="cell_hash")
    def hash(self) -> int:
        pass

    @typed_invokable(name="compute_data_size")
    def compute_data_size(self, max_cells: int) -> tuple[int, int, int]:
        pass

    @typed_invokable(name="compute_data_size?")
    def compute_data_size_check(
        self, max_cells: int,
    ) -> tuple[int, int, int, int]:
        pass

    @typed_invokable(name="set_data")
    def set_data(self) -> None:
        pass

    @typed_invokable(name="cell_depth")
    def depth(self) -> int:
        pass

    @typed_invokable(name="cell_null?")
    def is_null(self) -> int:
        pass

    @typed_invokable(name="send_raw_message")
    def send_raw_message(self, mode: int) -> None:
        pass

    @typed_invokable(name="set_code")
    def set_code(self) -> None:
        pass


class Dict(Cell):
    @classmethod
    def type_name(cls) -> str:
        return "cell"

    @typed_invokable(name="dict_set")
    def dict_set(
        self,
        key_len: int,
        index: "Slice",
        value: "Slice",
    ) -> "Dict":
        pass

    @typed_invokable(name="dict_set")
    def dict_set_(self, key_len: int, index: "Slice", value: "Slice") -> None:
        pass

    @typed_invokable(name="dict_set_builder")
    def dict_set_builder(
        self,
        key_len: int,
        index: "Slice",
        value: "Builder",
    ) -> "Dict":
        pass

    @typed_invokable(name="~dict_set_builder")
    def dict_set_builder_(
        self,
        key_len: int,
        index: "Slice",
        value: "Builder",
    ) -> None:
        pass

    @typed_invokable(name="dict_delete_get_min")
    def dict_delete_get_min(
        self,
        key_len: int,
    ) -> tuple["Dict", "Slice", "Slice", int]:
        pass

    @typed_invokable(name="dict::delete_get_min")
    def dict_delete_get_min_(
        self,
        key_len: int,
    ) -> tuple["Slice", "Slice", int]:
        pass

    @typed_invokable(name="dict_delete_get_max")
    def dict_delete_get_max(
        self,
        key_len: int,
    ) -> tuple["Dict", "Slice", "Slice", int]:
        pass

    @typed_invokable(name="dict::delete_get_max")
    def dict_delete_get_max_(
        self,
        key_len: int,
    ) -> tuple["Slice", "Slice", int]:
        pass

    @typed_invokable(name="dict_empty?")
    def dict_empty_check(self) -> int:
        pass


class UDict(Dict):
    @typed_invokable(name="udict_set_ref")
    def set_ref(self, key_len: int, index: int, value: "Cell") -> "UDict":
        pass

    @typed_invokable(name="udict_set_ref")
    def set_ref_(self, key_len: int, index: int, value: "Cell") -> None:
        pass

    @typed_invokable(name="udict_get_ref")
    def get_ref(self, key_len: int, index: int) -> "Cell":
        pass

    @typed_invokable(name="udict_get_ref?")
    def get_ref_check(self, key_len: int, index: int) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_set_get_ref")
    def set_get_ref(
        self,
        key_len: int,
        index: int,
        value: "Cell",
    ) -> tuple["UDict", "Cell"]:
        pass

    @typed_invokable(name="udict_set_get_ref")
    def set_get_ref_(self, key_len: int, index: int, value: "Cell") -> "Cell":
        pass

    @typed_invokable(name="udict_delete?")
    def delete_check(self, key_len: int, index: int) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_delete?")
    def delete_check_(self, key_len: int, index: int) -> int:
        pass

    @typed_invokable(name="udict_get?")
    def get_check(self, key_len: int, index: int) -> tuple["Slice", int]:
        pass

    @typed_invokable(name="udict_delete_get?")
    def delete_get_check(
        self,
        key_len: int,
        index: int,
    ) -> tuple["UDict", "Slice", int]:
        pass

    @typed_invokable(name="udict_delete_get?")
    def delete_get_check_(
        self,
        key_len: int,
        index: int,
    ) -> tuple["Slice", int]:
        pass

    @typed_invokable(name="udict_set")
    def set(self, key_len: int, index: int, value: "Slice") -> "UDict":
        pass

    @typed_invokable(name="udict_set")
    def set_(self, key_len: int, index: int, value: "Slice") -> None:
        pass

    @typed_invokable(name="udict_add?")
    def add_check(
        self,
        key_len: int,
        index: int,
        value: "Slice",
    ) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_add?")
    def add_check_(self, key_len: int, index: int, value: "Slice") -> int:
        pass

    @typed_invokable(name="udict_replace?")
    def replace_check(
        self,
        key_len: int,
        index: int,
        value: "Slice",
    ) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_replace?")
    def replace_check_(self, key_len: int, index: int, value: "Slice") -> int:
        pass

    @typed_invokable(name="udict_set_builder")
    def set_builder(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> "UDict":
        pass

    @typed_invokable(name="udict_set_builder")
    def set_builder_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> None:
        pass

    @typed_invokable(name="udict_add_builder?")
    def add_builder_check(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_replace_builder?")
    def replace_builder_check(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> tuple["UDict", int]:
        pass

    @typed_invokable(name="udict_add_builder?")
    def add_builder_check_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> int:
        pass

    @typed_invokable(name="udict_replace_builder?")
    def replace_builder_check_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> int:
        pass

    @typed_invokable(name="udict_delete_get_min")
    def delete_get_min(
        self,
        key_len: int,
    ) -> tuple["UDict", int, "Slice", int]:
        pass

    @typed_invokable(name="udict::delete_get_min")
    def delete_get_min_(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_delete_get_max")
    def delete_get_max(
        self,
        key_len: int,
    ) -> tuple["UDict", int, "Slice", int]:
        pass

    @typed_invokable(name="udict::delete_get_max")
    def delete_get_max_(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_min?")
    def get_min_check(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_max?")
    def get_max_check(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_min_ref?")
    def get_min_ref_check(self, key_len: int) -> tuple[int, "Cell", int]:
        pass

    @typed_invokable(name="udict_get_max_ref?")
    def get_max_ref_check(self, key_len: int) -> tuple[int, "Cell", int]:
        pass

    @typed_invokable(name="udict_get_next?")
    def get_next_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_nexteq?")
    def get_nexteq_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_prev?")
    def get_prev_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="udict_get_preveq?")
    def get_preveq_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass


class IDict(Dict):
    @typed_invokable(name="idict_set_ref")
    def set_ref(self, key_len: int, index: int, value: "Cell") -> "IDict":
        pass

    @typed_invokable(name="idict_set_ref")
    def set_ref_(self, key_len: int, index: int, value: "Cell") -> None:
        pass

    @typed_invokable(name="idict_get_ref")
    def get_ref(self, key_len: int, index: int) -> "Cell":
        pass

    @typed_invokable(name="idict_get_ref?")
    def get_ref_check(self, key_len: int, index: int) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_set_get_ref")
    def set_get_ref(
        self,
        key_len: int,
        index: int,
        value: "Cell",
    ) -> tuple["IDict", "Cell"]:
        pass

    @typed_invokable(name="idict_set_get_ref")
    def set_get_ref_(self, key_len: int, index: int, value: "Cell") -> "Cell":
        pass

    @typed_invokable(name="idict_delete?")
    def delete_check(self, key_len: int, index: int) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_delete?")
    def delete_check_(self, key_len: int, index: int) -> int:
        pass

    @typed_invokable(name="idict_get?")
    def get_check(self, key_len: int, index: int) -> tuple["Slice", int]:
        pass

    @typed_invokable(name="idict_delete_get?")
    def delete_get_check(
        self,
        key_len: int,
        index: int,
    ) -> tuple["IDict", "Slice", int]:
        pass

    @typed_invokable(name="idict_delete_get?")
    def delete_get_check_(
        self,
        key_len: int,
        index: int,
    ) -> tuple["Slice", int]:
        pass

    @typed_invokable(name="idict_set")
    def set(self, key_len: int, index: int, value: "Slice") -> "IDict":
        pass

    @typed_invokable(name="idict_set")
    def set_(self, key_len: int, index: int, value: "Slice") -> None:
        pass

    @typed_invokable(name="idict_add?")
    def add_check(
        self,
        key_len: int,
        index: int,
        value: "Slice",
    ) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_add?")
    def add_check_(self, key_len: int, index: int, value: "Slice") -> int:
        pass

    @typed_invokable(name="idict_replace?")
    def replace_check(
        self,
        key_len: int,
        index: int,
        value: "Slice",
    ) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_replace?")
    def replace_check_(self, key_len: int, index: int, value: "Slice") -> int:
        pass

    @typed_invokable(name="idict_set_builder")
    def set_builder(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> "IDict":
        pass

    @typed_invokable(name="idict_set_builder")
    def set_builder_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> None:
        pass

    @typed_invokable(name="idict_add_builder?")
    def add_builder_check(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_replace_builder?")
    def replace_builder_check(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> tuple["IDict", int]:
        pass

    @typed_invokable(name="idict_add_builder?")
    def add_builder_check_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> int:
        pass

    @typed_invokable(name="idict_replace_builder?")
    def replace_builder_check_(
        self,
        key_len: int,
        index: int,
        value: "Builder",
    ) -> int:
        pass

    @typed_invokable(name="idict_delete_get_min")
    def delete_get_min(
        self,
        key_len: int,
    ) -> tuple["IDict", int, "Slice", int]:
        pass

    @typed_invokable(name="idict::delete_get_min")
    def delete_get_min_(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_delete_get_max")
    def delete_get_max(
        self,
        key_len: int,
    ) -> tuple["IDict", int, "Slice", int]:
        pass

    @typed_invokable(name="idict::delete_get_max")
    def delete_get_max_(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_min?")
    def get_min_check(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_max?")
    def get_max_check(self, key_len: int) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_min_ref?")
    def get_min_ref_check(self, key_len: int) -> tuple[int, "Cell", int]:
        pass

    @typed_invokable(name="idict_get_max_ref?")
    def get_max_ref_check(self, key_len: int) -> tuple[int, "Cell", int]:
        pass

    @typed_invokable(name="idict_get_next?")
    def get_next_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_nexteq?")
    def get_nexteq_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_prev?")
    def get_prev_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass

    @typed_invokable(name="idict_get_preveq?")
    def get_preveq_check(
        self,
        key_len: int,
        pivot: int,
    ) -> tuple[int, "Slice", int]:
        pass


class PfxDict(Cell):
    @classmethod
    def type_name(cls) -> str:
        return "cell"

    @typed_invokable(name="pfxdict_get?")
    def pfxdict_get_check(
        self,
        key_len: int,
        key: "Slice",
    ) -> tuple["Slice", "Slice", "Slice", int]:
        pass

    @typed_invokable(name="pfxdict_set?")
    def pfxdict_set_check(
        self,
        key_len: int,
        key: "Slice",
        value: "Slice",
    ) -> tuple["PfxDict", int]:
        pass

    @typed_invokable(name="pfxdict_delete?")
    def pfxdict_delete_check(
        self,
        key_len: int,
        key: "Slice",
    ) -> tuple["PfxDict", int]:
        pass

    @typed_invokable(name="pfxdict_set?")
    def pfxdict_set_check_(
        self,
        key_len: int,
        key: "Slice",
        value: "Slice",
    ) -> int:
        pass

    @typed_invokable(name="pfxdict_delete?")
    def pfxdict_delete_check_(self, key_len: int, key: "Slice") -> int:
        pass


class Builder(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "builder"


class Tensor(Entity, tuple):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args)

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        data = kwargs.pop("data", None)
        super().__init__(data=data, name=name)

    @typed_invokable(name="store_maybe_ref")
    def write_maybe(self, c: Cell) -> "Builder":
        pass

    @typed_invokable(name="builder_refs")
    def refs_n(self) -> int:
        pass

    @typed_invokable(name="builder_bits")
    def bits_n(self) -> int:
        pass

    @typed_invokable(name="builder_depth")
    def depth(self) -> int:
        pass

    @typed_invokable(name="end_cell")
    def end(self) -> "Cell":
        pass

    @typed_invokable(name="store_ref")
    def ref(self, c: Cell) -> "Builder":
        pass

    @typed_invokable(name="store_uint")
    def uint(self, x: int, len_: int) -> "Builder":
        pass

    @typed_invokable(name="store_int")
    def int(self, x: int, len_: int) -> "Builder":
        pass

    @typed_invokable(name="store_slice")
    def slice(self, s: "Slice") -> "Builder":
        pass

    @typed_invokable(name="store_dict")
    def dict(self, c: "Cell") -> "Builder":
        pass

    @typed_invokable(name="store_coins")
    def coins(self, x: int) -> "Builder":
        pass

    @typed_invokable(name="builder_null?")
    def is_null(self) -> int:
        pass

    @typed_invokable(name="store_builder")
    def builder(self, from_: "Builder") -> "Builder":
        pass


class Tuple(Entity):
    @classmethod
    def type_name(cls) -> str:
        return "tuple"


Factory.register("Tensor", Tensor)
Factory.register("Tuple", Tuple)
Factory.register("Builder", Builder)
Factory.register("Dict", Dict)
Factory.register("UDict", UDict)
Factory.register("IDict", IDict)
Factory.register("PfxDict", PfxDict)
Factory.register("Slice", Slice)
Factory.register("Cell", Cell)
Factory.register("String", String)
Factory.register("Cont", Cont)
Factory.register("Int", Int)
