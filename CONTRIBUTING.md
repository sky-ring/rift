# Contributing to Rift

🎉 First off, thanks for taking the time to contribute! 🎉

Following these standards shows that you value the time of the developers that created and are developing this open source project.
In response, they should show you respect by addressing your issue, reviewing adjustments, and assisting you in finalizing your pull requests.

Rift is an open source framework, and we welcome community contributions!
Writing tutorials or blog entries, enhancing the documentation, submitting bug reports and feature requests, or writing code that can be incorporated into rift itself are all ways to contribute.

## Prerequisite
When contributing to this repository, please first discuss the change you wish to make by issue,
email, or any other method with the owners of this repository before making a change.

If you find a security vulnerability, do NOT open an issue.
Any security issues should be submitted directly to 
security@skyring.io In order to determine whether 
you are dealing with a security issue, ask yourself this question:

Does the framework's base implementations lead to a generated FunC Smart Contract that has security vulnerabilities?

If the answer is "yes", then you're probably dealing with a security issue.
Note that even if you answer "no" to the question,
you may still be dealing with a security issue, so if you're unsure, just email us at security@skyring.io

## Code Style
This project follows `black`, `flake8` for code style. You need to ensure compliance before submitting a PR. Proceed with the following procedure to install the requirements and check the style:
1. Install `black`
```bash
pip install black
```
2. Install `flake8`
```bash
pip install flake8
```
3. We use following `flake8` plugins, install them:
```
dlint~=0.12.0
flake8-bandit~=3.0.0
flake8-broken-line~=0.4.0
flake8-bugbear~=22.7.1
flake8-comprehensions~=3.10.0
flake8-darglint~=1.8.1
flake8-debugger~=4.1.2
flake8-docstrings~=1.6.0
pydocstyle~=6.1.1
flake8-eradicate~=1.2.1
flake8-string-format~=0.3.0
flake8_commas~=2.1.0
flake8_isort~=4.1.1
flake8_quotes~=3.3.1
mccabe~=0.6.1
naming~=0.12.1
pycodestyle~=2.8.0
pyflakes~=2.4.0
rst-docstrings~=0.2.6
```
4. At project's root run:
```
black .
flake8 .
```
5. Resolve the logged issues and rerun 4 again until there are no issues.
6. You're ready to submit your PR.

## Commits

We follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) guidelines for commit message and we'd encourage you to do so when contributing.

## How to contribute
If the suggestion is accepted after discussion in the issues, proceed with the following procedure for contribution:

1. Create your own fork of the code
2. Create new branch with proper name (related to issue)
3. Do the changes in the branch and push to your remote
4. Submit a PR 

## Feature Request
If you've ever wished for a feature that doesn't exist in Rift,
you're probably not alone. There must be others out there with similar needs.
Many of the features that exist in Rift today were created because our users saw a need for them.
Create an issue describing the feature you want to see, why you need it, and how it should work.

## Code of Conduct
Please note that this project is released with a [Contributor Code of Conduct](https://github.com/sky-ring/rift/blob/main/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
