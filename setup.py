from setuptools import find_packages, setup

setup(
    name="dBuilder-py",
    version="0.0.1",
    description="",
    license="MIT",
    packages=find_packages(),
    author="Amin Rezaei",
    author_email="AminRezaei0x443@gmail.com",
    keywords=[],
    entry_points={
        "console_scripts": [
            "dbuilder = dbuilder.cli.entry:entry",
        ],
    },
    url="https://github.com/decentralized-builder/dBuilder.py",
    install_requires=[],
    extras_require={},
)
