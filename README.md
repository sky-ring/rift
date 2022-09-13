<img align="left" width="64" height="64" src="./assets/rift-icon.png">

# Rift

[![PyPI version](https://img.shields.io/badge/rift--framework-0.7.1-informational?style=flat-square&color=FFFF91)](https://pypi.org/project/rift-framework/)
[![Telegram](https://img.shields.io/badge/Telegram-@rift__framework-informational?style=flat-square&color=0088cc)](https://t.me/d_builder)
> _A magical **Python3** -> **FunC** portal_

Rift is smart contract development framework in Python for [TON (The Open Network)](https://ton.org). Its purpose is to make the development, testing, and deployment procedures much easier!

## Goals
- To be a simple full-stack Python framework for developing on the TON ecosystem
- Make standard contract implementations available (similar to OpenZeppelin)
- Utilize Python's syntax to provide code reuse, understandable, and organized code that is simple to test

## Overview
Rift's main purpose is to make contract building simpler for TON by bypassing the steep learning curve of `FunC`. Rift, by exploiting Python's OOP features, will enable you to create with more ease and less worry. In Rift, here is how the [Simple wallet contract](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-code.fc) looks:

```python
from rift import *


class SimpleWallet(Contract):
    """
    Simple Wallet Contract.

    # config
    get-methods:
        - seq_no
        - public_key
    """

    class Data(Model):
        seq_no: uint32
        public_key: uint256

    class ExternalBody(Payload):
        signature: slice[512]
        seq_no: uint32
        valid_until: uint32

    data: Data

    def external_receive(
        ctx,
        in_msg: Slice,
    ) -> None:
        msg = ctx.ExternalBody(in_msg)
        assert msg.valid_until > std.now(), 35
        assert msg.seq_no == ctx.data.seq_no, 33
        assert std.check_signature(
            msg.hash(after="signature"),
            msg.signature,
            ctx.data.public_key,
        ), 34
        std.accept_message()
        while msg.refs():
            mode = msg >> uint8
            std.send_raw_message(msg >> Ref[Cell], mode)
        ctx.data.seq_no += 1
        ctx.data.save()
```

## Quick Start

0. Install `Python 3.10+`
1. Install `rift`
```bash
pip install rift-framework
# or from source
git clone https://github.com/decentralized-builder/rift
cd rift
pip install -e .
```
2. Initialize your project:
```bash
rift init <project-name>
```
3. Start developing your contracts in `<project>/contracts/`
4. Build contracts and get the `FunC` contracts in `<project>/build/`
```bash
# in project folder
rift build
```

## Standard Contracts Implementation
- [x] Jetton Implementation ([jetton-impl](https://github.com/decentralized-builder/jetton-impl))
- [ ] NFT Implementation
- [ ] DEX Implementation


## Documentation and Examples
Full documentation with specifications is being developed and will be available shortly!
Until then, you may look at standard contracts implementation; they cover the majority of the ideas required; if you're looking for more, take a glance at the 'test/' directory for some demonstrations of Rift's capabilities.

## Roadmap

### Milestone 1: Python Framework for contract development

- [x] Semi One-to-One mapping of functions and expressions (Base Compiler, Python -> FunC)
- [x] First higher layer over the base mappings to simplify type calls (leveraging OOP capabilities)
- [x] Second higher layer over the base, simplifying contract developments towards maximizing code reusability and simplicity (leveraging Meta programming capabilities)
- [x] Providing standard smart contracts implementation with Rift

### Milestone 2: deploying, testing, interaction capabilities
- [ ] Simple interaction interface with TON Blockchain
- [ ] Simple deploying options of developed contracts
- [ ] Testing framework for the contracts developed with Rift

## Contributing
If you're interested in contributing to Rift, please see [CONTRIBUTING.md](https://github.com/decentralized-builder/Rift.py/blob/main/CONTRIBUTING.md) for the necessary specifications and procedure.

## Supporters
Special thanks to the [TON Society](https://society.ton.org/) for their support and grant, without which the project would not be feasible.
