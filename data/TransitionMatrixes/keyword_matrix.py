from enum import IntEnum
import data.alphabet as alphabet

class KeywordStates(IntEnum):
    INI_STATE = 1
    N_STATE = 2      # Para "Num"
    N_STATE_2 = 3    # Para "Num"
    T_STATE = 4      # Para "Text", "True"
    TE_STATE = 5     # Para "Text"
    TR_STATE = 6     # Para "True"
    TEXT_STATE = 7   # Para "Text"
    TRUE_STATE = 8   # Para "True"
    B_STATE = 9      # Para "Bool"
    BO_STATE = 10    # Para "Bool"
    BOO_STATE = 11   # Para "Bool"
    W_STATE = 12     # Para "While", "Write"
    WH_STATE = 13    # Para "While"
    WR_STATE = 14    # Para "Write"
    WHI_STATE = 15   # Para "While"
    WRI_STATE = 16   # Para "Write"
    WHIL_STATE = 17  # Para "While"
    WRIT_STATE = 18  # Para "Write"
    F_STATE = 19     # Para "For", "False"
    FO_STATE = 20    # Para "For"
    FA_STATE = 21    # Para "False"
    FAL_STATE = 22   # Para "False"
    FALS_STATE = 23  # Para "False"
    I_STATE = 24     # Para "If"
    IF_STATE = 25    # Para "If"
    E_STATE = 26     # Para "Else"
    EL_STATE = 27    # Para "Else"
    ELS_STATE = 28   # Para "Else"
    R_STATE = 29     # Para "Read"
    RE_STATE = 30    # Para "Read"
    REA_STATE = 31   # Para "Read"
    END_STATE = 32
    ERROR_STATE = 33

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
        'u': KeywordStates.N_STATE_2
    },
    KeywordStates.N_STATE_2: {
        'm': KeywordStates.END_STATE  # "Num"
    },
    KeywordStates.T_STATE: {
        'e': KeywordStates.TE_STATE,  # Para "Text"
        'r': KeywordStates.TR_STATE   # Para "True"
    },
    KeywordStates.TE_STATE: {
        'x': KeywordStates.TEXT_STATE
    },
    KeywordStates.TEXT_STATE: {
        't': KeywordStates.END_STATE  # "Text"
    },
    KeywordStates.TR_STATE: {
        'u': KeywordStates.TRUE_STATE
    },
    KeywordStates.TRUE_STATE: {
        'e': KeywordStates.END_STATE  # "True"
    },
    KeywordStates.B_STATE: {
        'o': KeywordStates.BO_STATE
    },
    KeywordStates.BO_STATE: {
        'o': KeywordStates.BOO_STATE
    },
    KeywordStates.BOO_STATE: {
        'l': KeywordStates.END_STATE  # "Bool"
    },
    KeywordStates.W_STATE: {
        'h': KeywordStates.WH_STATE,  # Para "While"
        'r': KeywordStates.WR_STATE   # Para "Write"
    },
    KeywordStates.WH_STATE: {
        'i': KeywordStates.WHI_STATE
    },
    KeywordStates.WHI_STATE: {
        'l': KeywordStates.WHIL_STATE
    },
    KeywordStates.WHIL_STATE: {
        'e': KeywordStates.END_STATE  # "While"
    },
    KeywordStates.WR_STATE: {
        'i': KeywordStates.WRI_STATE
    },
    KeywordStates.WRI_STATE: {
        't': KeywordStates.WRIT_STATE
    },
    KeywordStates.WRIT_STATE: {
        'e': KeywordStates.END_STATE  # "Write"
    },
    KeywordStates.F_STATE: {
        'o': KeywordStates.FO_STATE,  # Para "For"
        'a': KeywordStates.FA_STATE   # Para "False"
    },
    KeywordStates.FO_STATE: {
        'r': KeywordStates.END_STATE  # "For"
    },
    KeywordStates.FA_STATE: {
        'l': KeywordStates.FAL_STATE
    },
    KeywordStates.FAL_STATE: {
        's': KeywordStates.FALS_STATE
    },
    KeywordStates.FALS_STATE: {
        'e': KeywordStates.END_STATE  # "False"
    },
    KeywordStates.I_STATE: {
        'f': KeywordStates.END_STATE  # "If"
    },
    KeywordStates.E_STATE: {
        'l': KeywordStates.EL_STATE
    },
    KeywordStates.EL_STATE: {
        's': KeywordStates.ELS_STATE
    },
    KeywordStates.ELS_STATE: {
        'e': KeywordStates.END_STATE  # "Else"
    },
    KeywordStates.R_STATE: {
        'e': KeywordStates.RE_STATE
    },
    KeywordStates.RE_STATE: {
        'a': KeywordStates.REA_STATE
    },
    KeywordStates.REA_STATE: {
        'd': KeywordStates.END_STATE  # "Read"
    }
}