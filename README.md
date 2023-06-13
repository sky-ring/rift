<img align="left" width="64" height="64" src="https://github.com/sky-ring/rift/blob/main/assets/rift-icon.png">

# Rift

[![PyPI version](https://img.shields.io/badge/rift--framework-1.0.0--rc1-informational?style=flat-square&color=FFFF91&labelColor=360825)](https://pypi.org/project/rift-framework/1.0.0rc1/)
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

> **Warning**
>
> **Rift**'s stable version is currently in release-candidate state, and we strongly advise thorough testing before transitioning to production. We are still in the process of battle-testing some internal modules, and we anticipate announcing a stable release in the near future. It is advisable to first deploy your contracts to `testnet` and test them meticulously before making the decision to move to production. Additionally, please verify the `FunC` contracts generated.

0. Install `Python 3.10+`
1. Install `rift`
    ```bash
    pip install rift-framework==1.0.0-rc1
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

- [*Step-by-Step with Rift: Simple Storage Contract*](https://docs.skyring.io/rift/step-by-step-guides/simple-storage-contract)
- Step-by-step guide on integrating `Rift` into existing `FunC` projects: *Coming Soon!*

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

### Milestone 3: Launching a Community-Powered Rift
In this milestone, we are thrilled to unveil the stable version of Rift, primed and ready for integration into real-world projects. Our vision is to foster a Rift ecosystem that thrives on the collective intelligence of its community. We are opening doors and creating avenues for our community members to contribute, refine, and evolve Rift. Here are some of the exciting initiatives we have in mind:

- [ ] **Rift Advancement Proposals (RAPs)**: A dynamic platform for you to propose and discuss enhancements for Rift. This is your chance to help shape the future of Rift!

- [ ] **Comprehensive Documentation**: We are committed to offering an in-depth, yet user-friendly guide that reveals the full potential of Rift. Explore the inner workings and capabilities of Rift with ease and precision.

- [ ] **Extensive Example Sets**: Gain a deeper understanding of Rift through practical examples that showcase its robust features and functionalities.

- [ ] **Multi-Contract Testing / Sandbox Integration**: Embrace a worry-free testing environment. Experiment, play, and validate your projects with our integrated sandbox feature.

Join us on this thrilling journey, shaping the future of Rift, one milestone at a time. We can't wait to see where your contributions will lead us next!


## Support the Project
1. If `Rift` has been a lifesaver for you, giving it a star on GitHub is the ultimate high five!
2. You can also show your love by contributing to `Rift` through code, ideas, or even a kind word.
3. Feeling extra generous? Treat `Rift` to a coffee by donating to this TON address: `EQAIhZCDT7-pvweWh6c_76X7Dnv6Qlzt7-l1NNP8upZ_Areu`
4. Finally, spreading the word about `Rift` is a big boost for the project and helps us reach more people.

## Contributing
If you're interested in contributing to Rift, please see [CONTRIBUTING.md](https://github.com/sky-ring/rift/blob/main/CONTRIBUTING.md) for the necessary specifications and procedures.

## Supporters
Special thanks to the [TON Society](https://society.ton.org/) for their support and grant, without which the project would not be feasible.
