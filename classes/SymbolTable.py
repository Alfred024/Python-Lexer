# classes/symbol_table.py

from typing import Dict, Optional
from classes.Token import Token, TokenCategory

class SymbolInfo:
    def __init__(self, name: str, var_type: str, declared_line: int):
        self.name = name
        self.var_type = var_type
        self.declared_line = declared_line

    def __repr__(self):
        return f"SymbolInfo(name={self.name!r}, type={self.var_type!r}, line={self.declared_line})"


class SymbolTable:
    def __init__(self):
        self._symbols: Dict[str, SymbolInfo] = {}

    def is_declared(self, name: str) -> bool:
        return name in self._symbols

    def declare(self, name: str, var_type: str, line: int) -> None:
        if self.is_declared(name):
            raise ValueError(f"Variable '{name}' ya declarada en línea {self._symbols[name].declared_line}")
        self._symbols[name] = SymbolInfo(name, var_type, line)

    def get(self, name: str) -> Optional[SymbolInfo]:
        return self._symbols.get(name)

    def is_valid(self, token: Token) -> bool:
        lexeme = token.value

        if token.token_type != TokenCategory.IDENTIFIER:
            return False
        if not lexeme.startswith("@"):
            return False
        if len(lexeme) > 16:
            return False
        if self.is_declared(lexeme):
            return False
        return True

    def all_symbols(self) -> Dict[str, SymbolInfo]:
        return dict(self._symbols)
