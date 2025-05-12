# data/TransitionMatrixes/Delimitator_matrix.py
from enum import IntEnum
<<<<<<< HEAD
import data.alphabet as alphabet
=======
import data.dictionary as dictionary
>>>>>>> 74db4672bad86f8c5fb1590428ace9c756181ab9

class DelimitatorStates(IntEnum):
    INI_STATE      = 1
    END_STATE      = 2
<<<<<<< HEAD
    ERROR_STATE    = 3

delim_chars = alphabet.alphabet['delim_chars']
=======

delim_chars = dictionary.dictionary['delim_chars']
>>>>>>> 74db4672bad86f8c5fb1590428ace9c756181ab9

delimitator_matrix = {
    DelimitatorStates.INI_STATE: {
        **{delim: DelimitatorStates.END_STATE for delim in delim_chars}
    },
<<<<<<< HEAD
    DelimitatorStates.END_STATE: {},
=======
>>>>>>> 74db4672bad86f8c5fb1590428ace9c756181ab9
}