from setuptools import find_packages, setup

setup(
    name="rift-framework",
    version="0.9.4",
    description="A magical Python3 -> TON portal",
    license="MIT",
    packages=find_packages(exclude=["test"]),
    author="Amin Rezaei",
    author_email="AminRezaei0x443@gmail.com",
    keywords=[],
    entry_points={
        "console_scripts": [
            "rift = rift.cli.entry:entry",
        ],
    },
    url="https://github.com/sky-ring/rift",
    install_requires=[],
    extras_require={},
)
