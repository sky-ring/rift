<img align="left" width="64" height="64" src="./assets/dbuilder-icon.png">

# dBuilder.py
[![PyPI version](https://img.shields.io/badge/pytorch--lit-0.1.0-informational?style=flat-square&color=FFFF91)](https://pypi.org/project/dbuilder/)
[![Telegram](https://img.shields.io/badge/Telegram-@d__builder-informational?style=flat-square&color=0088cc)](https://t.me/d_builder)

dBuilder.py is smart contract development framework in Python for [TON (The Open Network)](https://ton.org). It's goal is to make the development, testing, and deployment processes a lot easier!

## Goals
- Be an easy-to-use full-stack python framework for building on TON ecosystem
- Provide standard contract implementations (similar to OpenZeppelin)
- Utilize Python’s syntax capabilities to provide code reusing, readable and structured code that’s easy to test.

## Overview
dBuilder's main point is to simplify contract development for TON, bypassing the steep learning curve of `FunC`. In current version, one-to-one mapping of Python to FunC is implemented, which comes with no special simplifications. But, the higher layers over the base are in development. Currently, this is what [Simple wallet contract](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-code.fc) looks like with dBuilder:

```python
from dbuilder import method, method_id
from dbuilder.core.loop import while_
from dbuilder.func.contract import Contract
from dbuilder.types import Slice


class SimpleWallet(Contract):
    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        super(SimpleWallet, self).external_receive(
            in_msg,
        )
        signature = in_msg.load_bits_(512)
        cs = in_msg
        msg_seqno = cs.load_uint_(32)
        valid_until = cs.load_uint_(32)
        self.throw_if(35, valid_until <= self.now())
        ds = self.get_data().begin_parse()
        stored_seqno = ds.load_uint_(32)
        public_key = ds.load_uint_(256)
        ds.end_parse()
        self.throw_unless(33, msg_seqno == stored_seqno)
        self.throw_unless(
            34,
            self.check_signature(
                self.slice_hash(in_msg),
                signature,
                public_key,
            ),
        )
        self.accept_message()
        cs.touch_()
        with while_(cs.slice_refs()):
            mode = cs.load_uint_(8)
            self.send_raw_message(cs.load_ref_(), mode)
        cs.end_parse()
        self.set_data(
            self.begin_cell()
            .store_uint(stored_seqno + 1, 32)
            .store_uint(public_key, 256)
            .end_cell(),
        )

    @method_id
    @method
    def seqno(self) -> int:
        return self.get_data().begin_parse().preload_uint(32)

    @method_id
    @method
    def get_public_key(self) -> int:
        cs = self.get_data().begin_parse()
        cs.load_uint_(32)
        return cs.preload_uint(256)
```
Full documentation with details is under development and will be available soon!

## Quick Start

0. Install `Python 3.10+`
1. Install `dbuilder`
```bash
pip install dbuilder
# or from source
git clone https://github.com/decentralized-builder/dBuilder.py
cd dBuilder.py
pip install -e .
```
2. Initialize your project:
```bash
dbuilder init <project-name>
```
1. Start developing your contracts in `<project>/contracts/`
2. Build contracts and get the `FunC` contracts in `build`
```bash
# in project folder
dbuilder build
```

## Vision
As mentioned, dBuilder's main advantage is the simplifications which will be available upon development of higher levels. If you're curious what it will look like, here is a future vision for Simple wallet contract implementation:

```python
class SimpleWallet(Contract):
    class Data:
        seq_no: UInt(32)
        public_key: UInt(256)
        getters = [seq_no, public_key]

    class Message:
        signature: UInt(512)
        seq_no: UInt(32)
        valid_until: UInt(32)

    def external_receive(
        self,
        in_msg: Slice,
    ) -> None:
        msg = Message(in_msg)
        assert msg.valid_until > self.now(), 35
        assert msg.seq_no == self.data.seq_no, 33
        assert self.check_signature(
            msg.hash(after="signature"),
            msg.signature,
            self.data.public_key,
        ), 34
        self.accept_message()

        with msg.has_ref():
            mode = msg.uint(8)
            self.send_raw_message(msg.ref(), mode)

        self.data.seq_no += 1
        self.data.save()
```

## Roadmap

### Milestone 1: Python Framework for contract development

- [x] Semi One-to-One mapping of functions and expressions (Base Compiler, Python -> FunC)
- [ ] First higher layer over the base mappings to simplify type calls (leveraging OOP capabilities)
- [ ] Second higher layer over the base, simplifying contract developments towards maximizing code reusability and simplicity (leveraging Meta programming capabilities)
- [ ] Providing standard smart contracts implementation with dBuilder

### Milestone 2: deploying, testing, interaction capabilities
- [ ] Simple interaction interface with TON Blockchain
- [ ] Simple deploying options of developed contracts
- [ ] Testing framework for the contracts developed with dBuilder

## Contributing

Please read the specifications and procedure at [CONTRIBUTING.md](https://github.com/decentralized-builder/dBuilder.py/blob/main/CONTRIBUTING.md) If you're interested in contributing to dBuilder.

## Supporters

Special Thanks to [TON Society](https://society.ton.org/) for supporting the project and providing the grant, which without it the project wouldn't be possible.
