from enum import Enum
from classes.ErrorsStack import LexicalErrorCode

# TODO: Función para extraer la info. del error de un archivo txt.

class TokenError:
    def __init__(self, error_code : LexicalErrorCode = LexicalErrorCode.ERROR_UNDEFINED, message: str = '', line: int = -1, column: int = -1) -> None:
        self._code = error_code
        self._message = message
        self._line = line
        self._column = column

    def __str__(self) -> str:
        return (
            f'''
                ERROR {self._code}: ___({self._message})____[{self._line}, {self._column}]
            '''
        )

tk = TokenError(message='Desc. del error', line=1, column=1)
tk.__str__()

class TokenCategory(Enum):
    IDENTIFIER           = "IDENTIFIER"
    KEYWORD              = "KEYWORD"
    DATA_TYPE            = "DATA_TYPE"
    NUM                  = "NUM"
    TEXT                 = "TEXT"
    BOOL                 = "BOOL"
    COMMENT              = "COMMENT"
    OPERATOR             = "OPERATOR"
    ARIT_OPER            = "ARIT_OPER"
    REL_OPER             = "REL_OPER"
    LOG_OPER             = "LOG_OPER"
    ASIG_OPER            = "ASIG_OPER"
    INC_OPER             = "INC_OPER"
    DEC_OPER             = "DEC_OPER"
    DELIMITATOR          = "DELIMITATOR"
    DELIM_POINT          = "DELIM_POINT" 
    DELIM_PARENT_LEFT    = "DELIM_PARENT_LEFT"
    DELIM_PARENT_RIGHT   = "DELIM_PARENT_RIGHT"
    DELIM_BRACE_LEFT     = "DELIM_BRACE_LEFT"  
    DELIM_BRACE_RIGHT    = "DELIM_BRACE_RIGHT"
    WHITESPACE           = "WHITESPACE"
    ERROR                = "ERROR"

# DELIMS --> 0 -99
# KEYWORDS -> 100 - 199
# OPERS -> 200 -299
# LEX_ERROR -> 300 -399
# SINTACT_ERROR -> 400 -499
# 
# 1000 -> Idents

class TokenCode(Enum):
    IDENTIFIER           = 100
    KEYWORD              = 101
    DATA_TYPE            = 102
    
    NUM                  = 103
    TEXT                 = 104
    BOOL                 = 105
    
    COMMENT              = 106
    
    OPERATOR             = 107
    ARIT_OPER            = 108
    REL_OPER             = 109
    LOG_OPER             = 110
    ASIG_OPER            = 111
    INC_OPER             = 112
    DEC_OPER             = 113
    
    DELIMITATOR          = 114
    DELIM_POINT          = 115
    DELIM_PARENT_LEFT    = 116
    DELIM_PARENT_RIGHT   = 117
    DELIM_BRACE_LEFT     = 118
    DELIM_BRACE_RIGHT    = 119
    
    WHITESPACE           = 120
    
    ERROR                = 121
    NO_IDENTIFIED        = 122


class Token:
    def __init__(self, category: TokenCategory, code : TokenCode = TokenCode.NO_IDENTIFIED, value : str = '', row: int = -1, column: int = -1):
        self.category = category
        self.code = code
        self.value = value
        self.row = row
        self.column = column

    def __str__(self):
        return f"Token({self.category.value}, '{self.value}', row={self.row}, column={self.column})"