# data/TransitionMatrixes/Delimitator_matrix.py
from enum import IntEnum
import data.dictionary as dictionary

class DelimitatorStates(IntEnum):
    INI_STATE      = 1
    END_STATE      = 2

delim_chars = dictionary.dictionary['delim_chars']

delimitator_matrix = {
    DelimitatorStates.INI_STATE: {
        **{delim: DelimitatorStates.END_STATE for delim in delim_chars}
    },
    DelimitatorStates.END_STATE: {},
}