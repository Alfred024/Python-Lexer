from enum import Enum

class LexemeValid(Enum):
    CHECK = 'CHECK'
    VALID = 'VALID'

class Lexeme:
    def __init__(self, value: str, row: int = 0, col: int = 0):
        self.category = category
        self.value = value
        self.row = row
        self.col = col

    def __str__(self):
        return f"Token({self.category.value}, '{self.value}', row={self.row}, col={self.col})"