from enum import Enum

class TokenCategory(Enum):
    IDENTIFIER = "IDENTIFIER"
    TYPE = "TYPE"
    KEYWORD = "KEYWORD"
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    ERROR = "ERROR"

class Token:
    def __init__(self, category: TokenCategory, value: str, row: int = 0, col: int = 0):
        self.category = category
        self.value = value
        self.row = row
        self.col = col

    def __str__(self):
        return f"Token({self.category.value}, '{self.value}', row={self.row}, col={self.col})"