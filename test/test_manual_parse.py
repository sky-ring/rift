from rift.fift.types import Cell, Slice


def message_addr_int(s: Slice):
    tag = s.uint_(2)
    if tag == 0:
        return True, {
            "addr": "none",
        }
    if tag != 2:
        return False, "Not std address"
    s.uint_(1)  # anycast
    wc = s.uint_(8)
    addr = s.uint_(256)
    return True, {
        "wc": wc,
        "addr": addr,
    }


def parse_internal_message_info(s: Slice):
    t = s.uint_(1)
    if t != 0:
        return False, "Not an internal message"
    ihr_disabled = s.uint_(1)
    bounce = s.uint_(1)
    bounced = s.uint_(1)
    ok, src = message_addr_int(s)
    if not ok:
        return ok, src
    ok, dst = message_addr_int(s)
    if not ok:
        return ok, dst
    value = s.coin_()
    no_dict = s.uint(1)
    if no_dict == 1:
        return False, "This message has extra currencies"
    ihr_fee = s.coin_()
    fwd_fee = s.coin_()
    created_lt = s.uint_(64)
    created_at = s.uint_(32)
    return True, {
        "ihr_disabled": ihr_disabled,
        "bounce": bounce,
        "bounced": bounced,
        "src": src,
        "dst": dst,
        "value": value,
        "ihr_fee": ihr_fee,
        "fwd_fee": fwd_fee,
        "created_lt": created_lt,
        "created_at": created_at,
    }


def parse_internal_message(data: Cell):
    s = data.parse()
    ok, info = parse_internal_message_info(s)
    if not ok:
        return ok, info
    s_init = s.uint_(1)
    if s_init == 1:
        return False, "We don't support state init yet"
    b_either = s.uint_(1)
    if b_either == 1:
        s = s.ref_().parse()
    return {
        "info": info,
        "body": s,
    }


def test_manual_parse():
    data = Cell(
        __value__="te6ccgEBAgEANgABYmIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACIGAAAAAAAAAAAAAAAAAEBAAA=",
    )
    x = parse_internal_message(data)
    print(x)
