from enum import IntEnum
import data.dictionary as dictionary

class CommentStates(IntEnum):
    INI_STATE = 1
    BODY_STATE = 2
    END_STATE = 3

# Crear all_chars como una lista de caracteres individuales
all_chars = (
    list(dictionary.dictionary['chars']) +  # ['a', 'b', ..., 'Z']
    list(dictionary.dictionary['numbers']) +  # ['0', '1', ..., '9']
    list(dictionary.dictionary['delim_chars']) +  # ['(', ')', '{', '}', '.', ',']
    list(dictionary.dictionary['oper_chars']) +  # ['+', '-', '*', '/', '=', ...]
    dictionary.dictionary['spaces'] +  # ['\n', '\t', ' ']
    ['$', '@', '_']  # ['$', '@', '_']
)

comment_matrix = {
    CommentStates.INI_STATE: {
        '$': CommentStates.BODY_STATE
    },
    CommentStates.BODY_STATE: {
        **{char: CommentStates.BODY_STATE for char in all_chars if char != '\n'},
        '\n': CommentStates.END_STATE
    }
}