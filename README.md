<img align="left" width="64" height="64" src="https://github.com/sky-ring/rift/blob/main/assets/rift-icon.png">

# Rift

[![PyPI version](https://img.shields.io/badge/rift--framework-0.9.14-informational?style=flat-square&color=FFFF91&labelColor=360825)](https://pypi.org/project/rift-framework/)
[![Telegram](https://img.shields.io/badge/Telegram-@skyring__org-informational?style=flat-square&color=0088cc&labelColor=360825)](https://t.me/skyring_org)
[![Telegram](https://img.shields.io/badge/Docs-docs.skyring.io/rift-informational?style=flat-square&color=6A0F49&labelColor=360825)](https://docs.skyring.io/rift/)

> _A magical **Python3** -> **TON** portal_

Rift is a full-stack development framework for [TON (The Open Network)](https://ton.org) that makes it easy for developers to use Python to develop, test, and deploy smart contracts on the TON network. With Rift, you can leverage the simplicity and versatility of Python to build and interact with TON, without having to learn the complexities of FunC or Fift. For examples of how Rift simplifies these processes, visit [Rift's website](https://rift.skyring.io).

## Features

- Develop smart contracts using Python syntax and OOP features
- Interact with the TON network to query data and deploy contracts
- Test smart contracts with an easy-to-use testing framework
- Standalone framework that only requires `Python 3.10`
- Can be used at any stage of the project, from development to testing to deployment

## Quick Start

0. Install `Python 3.10+`
1. Install `rift`
    ```bash
    pip install rift-framework
    # or from source
    git clone https://github.com/sky-ring/rift
    cd rift
    pip install -e .
    ```
2. Initialize your project:
    ```bash
    rift init <project-name>
    ```
3. Develop your contracts in `<project>/contracts/`
4. Write your tests in `<project>/tests/`
5. Place your deploy scripts in `<project>/deployers/`
6. Use `rift` to build, test, or deploy:
    ```bash
    # in project folder
    # builds TARGET
    rift build TARGET
    # tests TARGET
    rift test TARGET
    # deploys TARGET
    rift deploy TARGET
    ```
7. For more information, visit the documentation website at [docs.skyring.io/rift](https://docs.skyring.io/rift).

## Guides

- Step-by-step guide on how to use `Rift` to develop on TON: [Link](https://rift.skyring.io/guide-full)
- Step-by-step guide on integrating `Rift` into existing `FunC` projects: [Link](https://rift.skyring.io/guide-func)

## Standard Contracts Implementation
- [x] Jetton Implementation ([jettons](https://github.com/sky-ring/jettons))
- [ ] NFT Implementation
- [ ] DEX Implementation


## Roadmap

### Milestone 1: Python Framework for Contract Development
- [x] Semi One-to-One Mapping of Functions and Expressions (Base Compiler, Python -> FunC)
- [x] First Higher Layer over the Base Mappings to Simplify Type Calls (leveraging OOP Capabilities)
- [x] Second Higher Layer over the Base, Simplifying Contract Development towards Maximizing Code Reusability and Simplicity (leveraging Meta Programming Capabilities)
- [x] Providing Standard Smart Contracts Implementation with Rift

### Milestone 2: Deploying, Testing, Interaction Capabilities
- [x] Simple Interaction Interface with TON Blockchain
- [x] Simple Deploying Options of Developed Contracts
- [x] Testing Framework for the Contracts Developed with Rift

### Milestone 3: What's Next?
- Stay Tuned! We have extra plans that we will share soon with the community to further develop `Rift`.

## Support the Project
1. If `Rift` has been a lifesaver for you, giving it a star on GitHub is the ultimate high five!
2. You can also show your love by contributing to `Rift` through code, ideas, or even a kind word.
3. Feeling extra generous? Treat `Rift` to a coffee by donating to this TON address: `EQAIhZCDT7-pvweWh6c_76X7Dnv6Qlzt7-l1NNP8upZ_Areu`
4. Finally, spreading the word about `Rift` is a big boost for the project and helps us reach more people.

## Contributing
If you're interested in contributing to Rift, please see [CONTRIBUTING.md](https://github.com/sky-ring/rift/blob/main/CONTRIBUTING.md) for the necessary specifications and procedures.

## Supporters
Special thanks to the [TON Society](https://society.ton.org/) for their support and grant, without which the project would not be feasible.
