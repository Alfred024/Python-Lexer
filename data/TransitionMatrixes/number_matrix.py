from enum import IntEnum
import data.alphabet as alphabet

class NumberStates(IntEnum):
    INI_STATE = 1
    INT_PART  = 2
    DOT       = 3
    DEC_PART  = 4
    END_STATE = 5

numbers = alphabet.alphabet['numbers']
spaces = alphabet.alphabet['spaces']
delims = alphabet.alphabet['delim_chars']
opers  = alphabet.alphabet['oper_chars']

number_matrix = {
    NumberStates.INI_STATE: {
        **{n: NumberStates.INT_PART for n in numbers},
    },
    NumberStates.INT_PART: {
        **{n: NumberStates.INT_PART for n in numbers},
        '.': NumberStates.DOT,
        **{s: NumberStates.END_STATE for s in spaces},
        **{d: NumberStates.END_STATE for d in delims},
        **{o: NumberStates.END_STATE for o in opers},
    },
    NumberStates.DOT: {
        **{n: NumberStates.DEC_PART for n in numbers},
    },
    NumberStates.DEC_PART: {
        **{n: NumberStates.DEC_PART for n in numbers},
        **{s: NumberStates.END_STATE for s in spaces},
        **{d: NumberStates.END_STATE for d in delims},
        **{o: NumberStates.END_STATE for o in opers},
    },
}
