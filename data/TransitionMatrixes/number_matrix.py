from enum import IntEnum
import data.alphabet as alphabet

class NumberStates(IntEnum):
    INI_STATE = 1
    END_STATE = 2
    ERROR_STATE = 3

numbers = alphabet.alphabet['numbers']

number_matrix = {
    NumberStates.INI_STATE: {
        **{number: NumberStates.INI_STATE for number in numbers},
    },
    NumberStates.END_STATE:{
        
    }
}
