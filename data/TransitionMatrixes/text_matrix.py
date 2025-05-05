# data/TransitionMatrixes/text_matrix.py
from enum import IntEnum

class TextStates(IntEnum):
    INI_STATE      = 1
    BODY_STATE     = 2
    END_STATE      = 3

ascii_characters = [chr(i) for i in range(128)]

text_matrix = {
    TextStates.INI_STATE: {
        '"': TextStates.BODY_STATE,
        "'": TextStates.BODY_STATE,
    },
    TextStates.BODY_STATE: {
        **{char: TextStates.BODY_STATE for char in ascii_characters},
        '"': TextStates.END_STATE,
        "'": TextStates.END_STATE
    },
}