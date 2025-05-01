from enum import Enum

class TokenCategory(Enum):
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    DATA_TYPE = "DATA_TYPE"
    NUM = "NUM"
    TEXT = "TEXT"
    BOOL = "BOOL"
    COMMENT = "COMMENT"
    OPERATOR = "OPERATOR"
    ARIT_OPER = "ARIT_OPER"
    REL_OPER = "REL_OPER"
    LOG_OPER = "LOG_OPER"
    ASIG_OPER = "ASIG_OPER"
    INC_OPER = "INC_OPER"
    DEC_OPER = "DEC_OPER"
    DELIMITATOR = "DELIMITATOR"
    DELIM_POINT = "DELIM_POINT" 
    DELIM_PARENT_LEFT = "DELIM_PARENT_LEFT"
    DELIM_PARENT_RIGHT = "DELIM_PARENT_RIGHT"
    DELIM_BRACE_LEFT = "DELIM_BRACE_LEFT"  
    DELIM_BRACE_RIGHT = "DELIM_BRACE_RIGHT"
    WHITESPACE = "WHITESPACE"
    ERROR = "ERROR"


class Token:
    def __init__(self, category: TokenCategory, value: str, row: int = 0, col: int = 0):
        self.category = category
        self.value = value
        self.row = row
        self.col = col

    def __str__(self):
        return f"Token({self.category.value}, '{self.value}', row={self.row}, col={self.col})"