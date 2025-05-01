# data/TransitionMatrixes/Operator_matrix.py
from enum import IntEnum
import data.dictionary as dictionary

class OperatorStates(IntEnum):
    INI_STATE      = 1
    STATE_A        = 2
    STATE_INC      = 3
    STATE_DEC      = 4
    STATE_REL      = 5
    STATE_REL_B    = 6
    STATE_LOG_AND  = 7
    STATE_LOG_OR   = 8
    END_STATE      = 9

numbers  = dictionary.dictionary['numbers']
spaces   = dictionary.dictionary['spaces']
operators   = dictionary.dictionary['oper_chars']
all_chars_valid = ['@'] + list(dictionary.dictionary['numbers']) + dictionary.dictionary['spaces']

operator_matrix = {
    OperatorStates.INI_STATE: {
        '+': OperatorStates.STATE_INC,
        '-': OperatorStates.STATE_DEC,
        **{char: OperatorStates.STATE_REL for char in ['!', '<', '>', '=']},
        **{operator: OperatorStates.STATE_A for operator in ['*', '/']},
        '&': OperatorStates.STATE_LOG_AND,
        '|': OperatorStates.STATE_LOG_OR,
    },
    OperatorStates.STATE_A: {
        **{char: OperatorStates.END_STATE for char in all_chars_valid},
    },
    OperatorStates.STATE_INC: {
        '+': OperatorStates.END_STATE,
        **{char: OperatorStates.END_STATE for char in all_chars_valid},
    },
    OperatorStates.STATE_DEC: {
        '-': OperatorStates.END_STATE,
        **{char: OperatorStates.END_STATE for char in all_chars_valid},
    },
    OperatorStates.STATE_REL: {
        '=': OperatorStates.END_STATE,
        **{char: OperatorStates.END_STATE for char in all_chars_valid},
    },
    OperatorStates.STATE_LOG_AND: {
        '&': OperatorStates.END_STATE,
        **{char: OperatorStates.END_STATE for char in all_chars_valid},
    },
    OperatorStates.STATE_LOG_OR: {
        '|': OperatorStates.END_STATE,
        **{char: OperatorStates.END_STATE for char in all_chars_valid},
    },
}