from rift import *
from rift.runtime.config import *


def test_msg_serialize():
    Config.mode = Mode.FIFT
    msg = InternalMessage.build(
        MsgAddress.std(0, 0),
        amount=100,
        bounce=0,
    )
    print(msg.as_cell())
