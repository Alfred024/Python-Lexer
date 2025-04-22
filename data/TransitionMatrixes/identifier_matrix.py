# data/TransitionMatrixes/identifier_matrix.py
from enum import IntEnum
import data.dictionary as dictionary

class IdentifierStates(IntEnum):
    INI_STATE      = 1
    PRE_BODY_STATE = 2
    BODY_STATE     = 3
    END_STATE      = 4

chars   = dictionary.dictionary['chars']
numbers  = dictionary.dictionary['numbers']
spaces  = dictionary.dictionary['spaces']

identifier_matrix = {
    IdentifierStates.INI_STATE: {
        '@': IdentifierStates.PRE_BODY_STATE
    },
    IdentifierStates.PRE_BODY_STATE: {
        **{char: IdentifierStates.BODY_STATE for char in chars},
        '_': IdentifierStates.BODY_STATE ,
        **{space: IdentifierStates.END_STATE for space in spaces},
        '.': IdentifierStates.END_STATE,
    },
    IdentifierStates.BODY_STATE: {
        **{char: IdentifierStates.BODY_STATE for char in chars},
        **{number: IdentifierStates.BODY_STATE for number in numbers},
        '_': IdentifierStates.BODY_STATE ,
        **{space: IdentifierStates.END_STATE for space in spaces},
        '.': IdentifierStates.END_STATE,
    },
}