# data/TransitionMatrixes/operator_matrix.py
from enum import IntEnum
import data.alphabet as alphabet

class OperatorStates(IntEnum):
    INI_STATE     = 1
    PLUS    = 2
    MINUS   = 3
    REL_1   = 4   # '!', '<', '>', '='
    AND_1   = 5   # '&'
    OR_1    = 6   # '|'
    END_STATE     = 7

operator_matrix = {
    OperatorStates.INI_STATE: {
        '+': OperatorStates.PLUS,
        '-': OperatorStates.MINUS,
        '*': OperatorStates.END_STATE,
        '/': OperatorStates.END_STATE,
        '!': OperatorStates.REL_1,
        '<': OperatorStates.REL_1,
        '>': OperatorStates.REL_1,
        '=': OperatorStates.REL_1,
        '&': OperatorStates.AND_1,
        '|': OperatorStates.OR_1,
    },

    # intentamos formar operadores de dos caracteres; si no coincide, terminamos
    OperatorStates.PLUS: {
        '+': OperatorStates.END_STATE          # '++'
    },
    OperatorStates.MINUS: {
        '-': OperatorStates.END_STATE          # '--'
    },
    OperatorStates.REL_1: {
        '=': OperatorStates.END_STATE          # '==', '!=', '<=', '>='
    },
    OperatorStates.AND_1: {
        '&': OperatorStates.END_STATE          # '&&'
    },
    OperatorStates.OR_1: {
        '|': OperatorStates.END_STATE          # '||'
    },

    # END_STATE no necesita transiciones
    OperatorStates.END_STATE: {}
}
