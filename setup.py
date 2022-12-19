from setuptools import setup
from build import build_kwargs

setup(
    name="rift-framework",
    version="0.9.5",
    description="A magical Python3 -> FunC portal",
    license="MIT",
    packages=["rift"],
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
    **build_kwargs(),
)
