from setuptools import find_packages, setup

setup(
    name="dbuilder",
    version="0.2.0",
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
