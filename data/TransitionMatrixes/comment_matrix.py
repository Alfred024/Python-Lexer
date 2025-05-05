from enum import IntEnum
import data.alphabet as alphabet

class CommentStates(IntEnum):
    INI_STATE = 1
    BODY_STATE = 2
    END_STATE = 3

# Crear all_chars como una lista de caracteres individuales
all_chars = (
    list(alphabet.alphabet['chars']) +  # ['a', 'b', ..., 'Z']
    list(alphabet.alphabet['numbers']) +  # ['0', '1', ..., '9']
    list(alphabet.alphabet['delim_chars']) +  # ['(', ')', '{', '}', '.', ',']
    list(alphabet.alphabet['oper_chars']) +  # ['+', '-', '*', '/', '=', ...]
    alphabet.alphabet['spaces'] +  # ['\n', '\t', ' ']
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