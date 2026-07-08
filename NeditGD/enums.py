from enum import Enum
from typing import Dict


def remove_enums(d: Dict):
    for k in d:
        v = d[k]
        if isinstance(v, Enum):
            d[k] = v.value


# item_type_1, ..2, ..3
class ItemType(Enum):
    COUNTER : int = 1
    TIMER   : int = 2
    POINTS  : int = 3
    TIME    : int = 4
    ATTEMPT : int = 5

# op_1, ..2, ..3
class OpType(Enum):
    NONE    : int = 0
    PLUS    : int = 1
    MINUS   : int = 2
    MUL     : int = 3
    DIV     : int = 4

# round_op_1, ..2
class RoundOpType(Enum):
    NONE    : int = 0
    ROUND   : int = 1
    FLOOR   : int = 2
    CEIL    : int = 3

# sign_op_1, ..2
class SignOpType(Enum):
    NONE    : int = 0
    ABS     : int = 1
    NEG     : int = 2


# cmp_op - specifically
class CmpType(Enum):
    EQ      : int = 0
    GT      : int = 1
    GE      : int = 2
    LT      : int = 3
    LE      : int = 4
    NE      : int = 5

    def to_instant_comp_value(self):
        return {
            CmpType.EQ: 0,
            CmpType.GT: 1,
            CmpType.LT: 2
        }[self]

    
    def negate(self):
        return {
            CmpType.EQ: CmpType.NE,
            CmpType.GT: CmpType.LE,
            CmpType.LT: CmpType.GE,
            CmpType.NE: CmpType.EQ,
            CmpType.LE: CmpType.GT,
            CmpType.GE: CmpType.LT,
        }[self]