from rift.core.annots import asm, impure
from rift.core.entity import Entity
from rift.func.library import Library
from rift.types.types import Builder, Cell, Cont, Slice, Tuple


# noinspection PyTypeChecker,SpellCheckingInspection,PyUnusedLocal
class Stdlib(Library):
    __ignore__ = True

    @asm()
    def null(self) -> Entity:
        return "NULL"

    @asm()
    def now(self) -> int:
        return "NOW"

    @asm()
    def my_address(self) -> Slice:
        return "MYADDR"

    @asm()
    def get_balance(self) -> Tuple:
        return "BALANCE"

    @asm()
    def cur_lt(self) -> int:
        return "LTIME"

    @asm()
    def block_lt(self) -> int:
        return "BLOCKLT"

    @asm()
    def cell_hash(self, c: Cell) -> int:
        return "HASHCU"

    @asm()
    def slice_hash(self, s: Slice) -> int:
        return "HASHSU"

    @asm()
    def string_hash(self, s: Slice) -> int:
        return "SHA256U"

    @asm()
    def check_signature(
        self,
        hash_: int,
        signature: Slice,
        public_key: int,
    ) -> int:
        return "CHKSIGNU"

    @asm()
    def check_data_signature(
        self,
        data: Slice,
        signature: Slice,
        public_key: int,
    ) -> int:
        return "CHKSIGNS"

    @impure
    @asm()
    def compute_data_size(
        self,
        c: Cell,
        max_cells: int,
    ) -> tuple[int, int, int]:
        return "CDATASIZE"

    @impure
    @asm()
    def slice_compute_data_size(
        self,
        s: Slice,
        max_cells: int,
    ) -> tuple[int, int, int]:
        return "SDATASIZE"

    @asm(name="compute_data_size?")
    def compute_data_size_check(
        self,
        c: Cell,
        max_cells: int,
    ) -> tuple[int, int, int, int]:
        return "CDATASIZEQ NULLSWAPIFNOT2 NULLSWAPIFNOT"

    @asm(name="slice_compute_data_size?")
    def slice_compute_data_size_check(
        self,
        c: Cell,
        max_cells: int,
    ) -> tuple[int, int, int, int]:
        return "SDATASIZEQ NULLSWAPIFNOT2 NULLSWAPIFNOT"

    @impure
    @asm()
    def throw_if(self, excno: int, cond: int) -> None:
        return "THROWARGIF"

    @impure
    @asm()
    def dump_stack(self) -> None:
        return "DUMPSTK"

    @asm()
    def get_data(self) -> Cell:
        return "c4 PUSH"

    @impure
    @asm()
    def set_data(self, c: Cell) -> None:
        return "c4 POP"

    @impure
    @asm()
    def get_c3(self) -> Cont:
        return "c3 PUSH"

    @impure
    @asm()
    def set_c3(self, c: Cont) -> None:
        return "c3 POP"

    @impure
    @asm()
    def bless(self, s: Slice) -> Cont:
        return "BLESS"

    @impure
    @asm()
    def accept_message(self) -> None:
        return "ACCEPT"

    @impure
    @asm()
    def set_gas_limit(self, limit: int) -> None:
        return "SETGASLIMIT"

    @impure
    @asm()
    def commit(self) -> None:
        return "COMMIT"

    @impure
    @asm()
    def buy_gas(self, gram: int) -> None:
        return "BUYGAS"

    @asm()
    def min(self, x: int, y: int) -> int:
        return "MIN"

    @asm()
    def max(self, x: int, y: int) -> int:
        return "MAX"

    @asm()
    def minmax(self, x: int, y: int) -> tuple[int, int]:
        return "MINMAX"

    @asm()
    def abs(self, x: int) -> int:
        return "ABS"

    @asm()
    def begin_parse(self, c: Cell) -> Slice:
        return "CTOS"

    @impure
    @asm()
    def end_parse(self, s: Slice) -> None:
        return "ENDS"

    @asm(out_order=(1, 0))
    def load_ref(self, s: Slice) -> tuple[Slice, Cell]:
        return "LDREF"

    @asm()
    def preload_ref(self, s: Slice) -> Cell:
        return "PLDREF"

    @asm(input_order=("s", "len_"), out_order=(1, 0), name="~load_int")
    def load_int_(self, s: Slice, len_: int) -> int:
        return "LDIX"

    @asm(out_order=(1, 0), name="~load_uint")
    def load_uint_(self, s: Slice, len_: int) -> int:
        return "LDUX"

    @asm()
    def preload_int(self, s: Slice, len_: int) -> int:
        return "PLDIX"

    @asm()
    def preload_uint(self, s: Slice, len_: int) -> int:
        return "PLDUX"

    @asm(input_order=("s", "len_"), out_order=(1, 0))
    def load_bits(self, s: Slice, len_: int) -> tuple[Slice, Slice]:
        return "LDSLICEX"

    @asm()
    def preload_bits(self, s: Slice, len_: int) -> Slice:
        return "PLDSLICEX"

    @asm(out_order=(1, 0))
    def load_grams(self, s: Slice) -> tuple[Slice, int]:
        return "LDGRAMS"

    @asm()
    def skip_bits(self, s: Slice, len_: int) -> Slice:
        return "SDSKIPFIRST"

    @asm(name="~skip_bits")
    def skip_bits_(self, s: Slice, len_: int) -> None:
        return "SDSKIPFIRST"

    @asm()
    def first_bits(self, s: Slice, len_: int) -> Slice:
        return "SDCUTFIRST"

    @asm()
    def skip_last_bits(self, s: Slice, len_: int) -> Slice:
        return "SDSKIPLAST"

    @asm(name="~skip_last_bits")
    def skip_last_bits_(self, s: Slice, len_: int) -> None:
        return "SDSKIPLAST"

    @asm()
    def slice_last(self, s: Slice, len_: int) -> Slice:
        return "SDCUTLAST"

    @asm(out_order=(1, 0))
    def load_dict(self, s: Slice) -> tuple[Slice, Cell]:
        return "LDDICT"

    @asm()
    def preload_dict(self, s: Slice) -> Cell:
        return "PLDDICT"

    @asm()
    def skip_dict(self, s: Slice) -> Slice:
        return "SKIPDICT"

    @asm(out_order=(1, 0))
    def load_maybe_ref(self, s: Slice) -> tuple[Slice, Cell]:
        return "LDOPTREF"

    @asm()
    def preload_maybe_ref(self, s: Slice) -> Cell:
        return "PLDOPTREF"

    @asm(input_order=("c", "b"))
    def store_maybe_ref(self, b: Builder, c: Cell) -> Builder:
        return "STOPTREF"

    @asm()
    def cell_depth(self, c: Cell) -> int:
        return "CDEPTH"

    @asm()
    def slice_refs(self, s: Slice) -> int:
        return "SREFS"

    @asm()
    def slice_bits(self, s: Slice) -> int:
        return "SBITS"

    @asm()
    def slice_bits_refs(self, s: Slice) -> tuple[int, int]:
        return "SBITREFS"

    @asm(name="slice_empty?")
    def slice_empty_check(self, s: Slice) -> int:
        return "SEMPTY"

    @asm(name="slice_data_empty?")
    def slice_data_empty_check(self, s: Slice) -> int:
        return "SDEMPTY"

    @asm(name="slice_refs_empty?")
    def slice_refs_empty_check(self, s: Slice) -> int:
        return "SREMPTY"

    @asm()
    def slice_depth(self, s: Slice) -> int:
        return "SDEPTH"

    @asm()
    def builder_refs(self, b: Builder) -> int:
        return "BREFS"

    @asm()
    def builder_bits(self, b: Builder) -> int:
        return "BBITS"

    @asm()
    def builder_depth(self, b: Builder) -> int:
        return "BDEPTH"

    @asm()
    def begin_cell(self) -> Builder:
        return "NEWC"

    @asm()
    def end_cell(self, b: Builder) -> Cell:
        return "ENDC"

    @asm(input_order=("c", "b"))
    def store_ref(self, b: Builder, c: Cell) -> Builder:
        return "STREF"

    @asm(input_order=("x", "b", "len_"))
    def store_uint(self, b: Builder, x: int, len_: int) -> Builder:
        return "STUX"

    @asm(input_order=("x", "b", "len_"))
    def store_int(self, b: Builder, x: int, len_: int) -> Builder:
        return "STIX"

    @asm()
    def store_slice(self, b: Builder, s: Slice) -> Builder:
        return "STSLICER"

    @asm()
    def store_grams(self, b: Builder, x: int) -> Builder:
        return "STGRAMS"

    @asm(input_order=("c", "b"))
    def store_dict(self, b: Builder, c: Cell) -> Builder:
        return "STDICT"

    @asm(out_order=(1, 0))
    def load_msg_addr(self, s: Slice) -> tuple[Slice, Slice]:
        return "LDMSGADDR"

    @asm()
    def parse_addr(self, s: Slice) -> Tuple:
        return "PARSEMSGADDR"

    @asm()
    def parse_std_addr(self, s: Slice) -> tuple[int, int]:
        return "REWRITESTDADDR"

    @asm()
    def parse_var_addr(self, s: Slice) -> tuple[int, Slice]:
        return "REWRITEVARADDR"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def idict_set_ref(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Cell,
    ) -> Cell:
        return "DICTISETREF"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="~idict_set_ref",
    )
    def idict_set_ref_(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Cell,
    ) -> None:
        return "DICTISETREF"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def udict_set_ref(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Cell,
    ) -> Cell:
        return "DICTUSETREF"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="~udict_set_ref",
    )
    def udict_set_ref_(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Cell,
    ) -> None:
        return "DICTUSETREF"

    @asm(input_order=("index", "dict_", "key_len"))
    def idict_get_ref(self, dict_: Cell, key_len: int, index: int) -> Cell:
        return "DICTIGETOPTREF"

    @asm(input_order=("index", "dict_", "key_len"), name="idict_get_ref?")
    def idict_get_ref_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Cell, int]:
        return "DICTIGETREF"

    @asm(input_order=("index", "dict_", "key_len"), name="udict_get_ref?")
    def udict_get_ref_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Cell, int]:
        return "DICTUGETREF"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def idict_set_get_ref(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Cell,
    ) -> tuple[Cell, Cell]:
        return "DICTISETGETOPTREF"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def udict_set_get_ref(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Cell,
    ) -> tuple[Cell, Cell]:
        return "DICTUSETGETOPTREF"

    @asm(input_order=("index", "dict_", "key_len"), name="idict_delete?")
    def idict_delete_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Cell, int]:
        return "DICTIDEL"

    @asm(input_order=("index", "dict_", "key_len"), name="udict_delete?")
    def udict_delete_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Cell, int]:
        return "DICTUDEL"

    @asm(input_order=("index", "dict_", "key_len"), name="idict_get?")
    def idict_get_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Slice, int]:
        return "DICTIGET", "NULLSWAPIFNOT"

    @asm(input_order=("index", "dict_", "key_len"), name="udict_get?")
    def udict_get_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Slice, int]:
        return "DICTUGET", "NULLSWAPIFNOT"

    @asm(input_order=("index", "dict_", "key_len"), name="idict_delete_get?")
    def idict_delete_get_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Cell, Slice, int]:
        return "DICTIDELGET", "NULLSWAPIFNOT"

    @asm(input_order=("index", "dict_", "key_len"), name="udict_delete_get?")
    def udict_delete_get_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Cell, Slice, int]:
        return "DICTUDELGET", "NULLSWAPIFNOT"

    @asm(input_order=("index", "dict_", "key_len"), name="~idict_delete_get?")
    def idict_delete_get_check_(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Slice, int]:
        return "DICTIDELGET", "NULLSWAPIFNOT"

    @asm(input_order=("index", "dict_", "key_len"), name="~udict_delete_get?")
    def udict_delete_get_check_(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
    ) -> tuple[Slice, int]:
        return "DICTUDELGET", "NULLSWAPIFNOT"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def udict_set(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Slice,
    ) -> Cell:
        return "DICTUSET"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="~udict_set",
    )
    def udict_set_(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Slice,
    ) -> None:
        return "DICTUSET"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def idict_set(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Slice,
    ) -> Cell:
        return "DICTISET"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="~idict_set",
    )
    def idict_set_(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Slice,
    ) -> None:
        return "DICTISET"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def dict_set(
        self,
        dict_: Cell,
        key_len: int,
        index: Slice,
        value: Slice,
    ) -> Cell:
        return "DICTSET"

    @asm(input_order=("value", "index", "dict_", "key_len"), name="~dict_set")
    def dict_set_(
        self,
        dict_: Cell,
        key_len: int,
        index: Slice,
        value: Slice,
    ) -> None:
        return "DICTSET"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="udict_add?",
    )
    def udict_add_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Slice,
    ) -> tuple[Cell, int]:
        return "DICTUADD"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="udict_replace?",
    )
    def udict_replace_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Slice,
    ) -> tuple[Cell, int]:
        return "DICTUREPLACE"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="idict_add?",
    )
    def idict_add_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Slice,
    ) -> tuple[Cell, int]:
        return "DICTIADD"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="idict_replace?",
    )
    def idict_replace_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Slice,
    ) -> tuple[Cell, int]:
        return "DICTIREPLACE"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def udict_set_builder(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Builder,
    ) -> Cell:
        return "DICTUSETB"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="~udict_set_builder",
    )
    def udict_set_builder_(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Builder,
    ) -> None:
        return "DICTUSETB"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def idict_set_builder(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Builder,
    ) -> Cell:
        return "DICTISETB"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="~idict_set_builder",
    )
    def idict_set_builder_(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Builder,
    ) -> None:
        return "DICTISETB"

    @asm(input_order=("value", "index", "dict_", "key_len"))
    def dict_set_builder(
        self,
        dict_: Cell,
        key_len: int,
        index: Slice,
        value: Builder,
    ) -> Cell:
        return "DICTSETB"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="~dict_set_builder",
    )
    def dict_set_builder_(
        self,
        dict_: Cell,
        key_len: int,
        index: Slice,
        value: Builder,
    ) -> None:
        return "DICTSETB"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="udict_add_builder?",
    )
    def udict_add_builder_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Builder,
    ) -> tuple[Cell, int]:
        return "DICTUADDB"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="udict_replace_builder?",
    )
    def udict_replace_builder_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Builder,
    ) -> tuple[Cell, int]:
        return "DICTUREPLACEB"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="idict_add_builder?",
    )
    def idict_add_builder_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Builder,
    ) -> tuple[Cell, int]:
        return "DICTIADDB"

    @asm(
        input_order=("value", "index", "dict_", "key_len"),
        name="idict_replace_builder?",
    )
    def idict_replace_builder_check(
        self,
        dict_: Cell,
        key_len: int,
        index: int,
        value: Builder,
    ) -> tuple[Cell, int]:
        return "DICTIREPLACEB"

    @asm(out_order=(0, 2, 1, 3))
    def udict_delete_get_min(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[Cell, int, Slice, int]:
        return "DICTUREMMIN", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3), name="~udict::delete_get_min")
    def udict_delete_get_min_(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Slice, int]:
        return "DICTUREMMIN", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3))
    def idict_delete_get_min(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[Cell, int, Slice, int]:
        return "DICTIREMMIN", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3), name="~idict::delete_get_min")
    def idict_delete_get_min_(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIREMMIN", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3))
    def dict_delete_get_min(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[Cell, Slice, Slice, int]:
        return "DICTREMMIN", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3), name="~dict::delete_get_min")
    def dict_delete_get_min_(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[Slice, Slice, int]:
        return "DICTREMMIN", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3))
    def udict_delete_get_max(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[Cell, int, Slice, int]:
        return "DICTUREMMAX", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3), name="~udict::delete_get_max")
    def udict_delete_get_max_(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Slice, int]:
        return "DICTUREMMAX", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3))
    def idict_delete_get_max(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[Cell, int, Slice, int]:
        return "DICTIREMMAX", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3), name="~idict::delete_get_max")
    def idict_delete_get_max_(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIREMMAX", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3))
    def dict_delete_get_max(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[Cell, Slice, Slice, int]:
        return "DICTREMMAX", "NULLSWAPIFNOT2"

    @asm(out_order=(0, 2, 1, 3), name="~dict::delete_get_max")
    def dict_delete_get_max_(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[Slice, Slice, int]:
        return "DICTREMMAX", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="udict_get_min?")
    def udict_get_min_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Slice, int]:
        return "DICTUMIN", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="udict_get_max?")
    def udict_get_max_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Slice, int]:
        return "DICTUMAX", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="udict_get_min_ref?")
    def udict_get_min_ref_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Cell, int]:
        return "DICTUMINREF", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="udict_get_max_ref?")
    def udict_get_max_ref_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Cell, int]:
        return "DICTUMAXREF", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="idict_get_min?")
    def idict_get_min_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIMIN", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="idict_get_max?")
    def idict_get_max_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIMAX", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="idict_get_min_ref?")
    def idict_get_min_ref_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Cell, int]:
        return "DICTIMINREF", "NULLSWAPIFNOT2"

    @asm(out_order=(1, 0, 2), name="idict_get_max_ref?")
    def idict_get_max_ref_check(
        self,
        dict_: Cell,
        key_len: int,
    ) -> tuple[int, Cell, int]:
        return "DICTIMAXREF", "NULLSWAPIFNOT2"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="udict_get_next?",
    )
    def udict_get_next_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTUGETNEXT", "NULLSWAPIFNOT2"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="udict_get_nexteq?",
    )
    def udict_get_nexteq_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTUGETNEXTEQ", "NULLSWAPIFNOT2"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="udict_get_prev?",
    )
    def udict_get_prev_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTUGETPREV", "NULLSWAPIFNOT2"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="udict_get_preveq?",
    )
    def udict_get_preveq_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTUGETPREVEQ", "NULLSWAPIFNOT2"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="idict_get_next?",
    )
    def idict_get_next_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIGETNEXT", "NULLSWAPIFNOT2"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="idict_get_nexteq?",
    )
    def idict_get_nexteq_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIGETNEXTEQ", "NULLSWAPIFNOT2"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="idict_get_prev?",
    )
    def idict_get_prev_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIGETPREV", "NULLSWAPIFNOT2"

    @asm(
        input_order=("pivot", "dict_", "key_len"),
        out_order=(1, 0, 2),
        name="idict_get_preveq?",
    )
    def idict_get_preveq_check(
        self,
        dict_: Cell,
        key_len: int,
        pivot: int,
    ) -> tuple[int, Slice, int]:
        return "DICTIGETPREVEQ", "NULLSWAPIFNOT2"

    @asm()
    def new_dict(self) -> Cell:
        return "NEWDICT"

    @asm(name="dict_empty?")
    def dict_empty_check(self, c: Cell) -> int:
        return "DICTEMPTY"

    @asm(input_order=("key", "dict_", "key_len"), name="pfxdict_get?")
    def pfxdict_get_check(
        self,
        dict_: Cell,
        key_len: int,
        key: Slice,
    ) -> tuple[Slice, Slice, Slice, int]:
        return "PFXDICTGETQ", "NULLSWAPIFNOT2"

    @asm(
        input_order=("value", "key", "dict_", "key_len"),
        name="pfxdict_set?",
    )
    def pfxdict_set_check(
        self,
        dict_: Cell,
        key_len: int,
        key: Slice,
        value: Slice,
    ) -> tuple[Cell, int]:
        return "PFXDICTSET"

    @asm(input_order=("key", "dict_", "key_len"), name="pfxdict_delete?")
    def pfxdict_delete_check(
        self,
        dict_: Cell,
        key_len: int,
        key: Slice,
    ) -> tuple[Cell, int]:
        return "PFXDICTDEL"

    @asm()
    def config_param(self, x: int) -> Cell:
        return "CONFIGOPTPARAM"

    @asm(name="cell_null?")
    def cell_null_check(self, c: Cell) -> int:
        return "ISNULL"

    @impure
    @asm()
    def raw_reserve(self, amount: int, mode: int) -> None:
        return "RAWRESERVE"

    @impure
    @asm()
    def raw_reserve_extra(
        self,
        amount: int,
        extra_amount: Cell,
        mode: int,
    ) -> None:
        return "RAWRESERVEX"

    @impure
    @asm()
    def send_raw_message(self, msg: Cell, mode: int) -> None:
        return "SENDRAWMSG"

    @impure
    @asm()
    def set_code(self, new_code: Cell) -> None:
        return "SETCODE"

    @impure
    @asm()
    def random(self) -> int:
        return "RANDU256"

    @impure
    @asm()
    def rand(self, range_: int) -> int:
        return "RAND"

    @impure
    @asm()
    def get_seed(self) -> int:
        return "RANDSEED"

    @impure
    @asm()
    def set_seed(self) -> int:
        return "SETRAND"

    @impure
    @asm()
    def randomize(self, x: int) -> None:
        return "ADDRAND"

    @impure
    @asm()
    def randomize_lt(self) -> None:
        return "LTIME", "ADDRAND"

    @asm()
    def store_coins(self, b: Builder, x: int) -> Builder:
        return "STVARUINT16"

    @asm(out_order=(1, 0))
    def load_coins(self, s: Slice) -> tuple[Slice, int]:
        return "LDVARUINT16"

    @asm()
    def equal_slices(self, a: Slice, b: Slice) -> int:
        return "SDEQ"

    @asm(name="builder_null?")
    def builder_null_check(self, b: Builder) -> int:
        return "ISNULL"

    @asm()
    def store_builder(self, to: Builder, from_: Builder) -> Builder:
        return "STBR"


std = Stdlib()
