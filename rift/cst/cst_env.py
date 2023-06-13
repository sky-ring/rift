import os


def cst_use_native():
    os.environ["LIBCST_PARSER_TYPE"] = "native"  # To support py >3.9
