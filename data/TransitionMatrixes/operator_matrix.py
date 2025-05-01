# data/TransitionMatrixes/Operator_matrix.py
from enum import IntEnum
import data.dictionary as dictionary

class OperatorStates(IntEnum):
    INI_STATE      = 1
    STATE_A        = 2
    STATE_B        = 3
    STATE_PLUS     = 3
    STATE_DEC      = 3
    STATE_EQUAL    = 3
    STATE_OPER     = 3
    STATE_REL      = 3
    END_STATE      = 4

operators   = dictionary.dictionary['oper_chars']
spaces   = dictionary.dictionary['spaces']

Operator_matrix = {
    OperatorStates.INI_STATE: {
        **{operator: OperatorStates.STATE_A for operator in ['+', '-', '=', '!', '<', '>', '&', '|',]},
        **{operator: OperatorStates.END_STATE for operator in ['*', '/']},
    },
    OperatorStates.STATE_A: {
        **{char: OperatorStates.STATE_PLUS for char in ['+']},
        **{char: OperatorStates.STATE_DEC for char in ['-']},
        **{char: OperatorStates.STATE_EQUAL for char in ['=']},
    },
    OperatorStates.STATE_PLUS: {
        '+': OperatorStates.END_STATE,
        **{space: OperatorStates.END_STATE for space in spaces},
    },
    OperatorStates.STATE_DEC: {
        '-': OperatorStates.END_STATE,
        **{space: OperatorStates.END_STATE for space in spaces},
    },
    OperatorStates.STATE_EQUAL: {
        '=': OperatorStates.STATE_REL,
        **{space: OperatorStates.END_STATE for space in spaces},
    },
    OperatorStates.STATE_OPER: {
        **{space: OperatorStates.END_STATE for space in spaces},
    },
    OperatorStates.STATE_REL: {
        **{space: OperatorStates.END_STATE for space in spaces},
    },
}