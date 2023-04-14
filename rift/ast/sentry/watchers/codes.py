from enum import Enum


class ErrorCode(Enum):
    RestrictUnknown = 1000
    UnSupportedFlow = 1001
    NoAsync = 1002
    NoMatch = 1003
    NoDelete = 1004
    NoWith = 1005
    NoYield = 1006
    NoTry = 1007
    NoNonLocal = 1008
    NoNamedExpr = 1009
    NoLambda = 1010
    NoIfExpr = 1011
    NoFStr = 1012
    NoStarredStatement = 1013
    NoSlicing = 1014
    NoComprehension = 1015
