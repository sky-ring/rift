from stdlib import throw_unless, store_data, UInt, Address, Dict, get_method, SmartContract, internal


class SimpleStorage(Contract):
    a: UInt(64)
    b: UInt(64)
    admin: Address

    @get_method
    def numbers(self):
        return self.a, self.b

    @internal
    def change_numbers(self, a: UInt(64), b: UInt(64)):
        sender = self.msg.sender
        throw_unless(701, sender == self.admin)
        self.a = a
        self.b = b
        self.save_state()
