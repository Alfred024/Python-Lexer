from enum import IntEnum
import data.alphabet as alphabet

class KeywordStates(IntEnum):
    INI_STATE = 1
    N_STATE = 2  # Para "Num"
    T_STATE = 3  # Para "Text", "True"
    B_STATE = 4  # Para "Bool"
    W_STATE = 5  # Para "While", "Write"
    F_STATE = 6  # Para "For", "False"
    I_STATE = 7  # Para "If"
    E_STATE = 8  # Para "Else"
    R_STATE = 9  # Para "Read"
    END_STATE = 10

keyword_matrix = {
    KeywordStates.INI_STATE: {
        'N': KeywordStates.N_STATE,
        'T': KeywordStates.T_STATE,
        'B': KeywordStates.B_STATE,
        'W': KeywordStates.W_STATE,
        'F': KeywordStates.F_STATE,
        'I': KeywordStates.I_STATE,
        'E': KeywordStates.E_STATE,
        'R': KeywordStates.R_STATE
    },
    KeywordStates.N_STATE: {
        'u': KeywordStates.END_STATE  # "Nu" -> "Num"
    },
    KeywordStates.T_STATE: {
        'e': KeywordStates.END_STATE,  # "Te" -> "Text"
        'r': KeywordStates.END_STATE  # "Tr" -> "True"
    },
    KeywordStates.B_STATE: {
        'o': KeywordStates.END_STATE  # "Bo" -> "Bool"
    },
    KeywordStates.W_STATE: {
        'h': KeywordStates.END_STATE,  # "Wh" -> "While"
        'r': KeywordStates.END_STATE  # "Wr" -> "Write"
    },
    KeywordStates.F_STATE: {
        'o': KeywordStates.END_STATE,  # "Fo" -> "For"
        'a': KeywordStates.END_STATE  # "Fa" -> "False"
    },
    KeywordStates.I_STATE: {
        'f': KeywordStates.END_STATE  # "If"
    },
    KeywordStates.E_STATE: {
        'l': KeywordStates.END_STATE  # "El" -> "Else"
    },
    KeywordStates.R_STATE: {
        'e': KeywordStates.END_STATE  # "Re" -> "Read"
    }
}