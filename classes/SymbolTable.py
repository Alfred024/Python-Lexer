from typing import Dict, List, Optional
from classes.Token import Token, TokenCategory

class SymbolInfo:
    def __init__(self, name: str, var_type: str, declared_line: int, value):
        self.name = name
        self.var_type = var_type
        self.declared_line = declared_line
        self.value = value
        
    def set_default(self):
        if self.var_type == "Num":
            self.value = 0
        elif self.var_type == "Bool":
            self.value = False
        elif self.var_type == "Text":
            self.value = ""
        else:
            self.value = None

    def __repr__(self):
        return f"SymbolInfo(name={self.name!r}, type={self.var_type!r}, line={self.declared_line})"

class SymbolTable:
    def __init__(self):
        self.tokens: List[Token] = []
        self._symbols: Dict[str, SymbolInfo] = {}

    def add_token(self, token: Token) -> None:
        self.tokens.append(token)

    def is_declared(self, name: str) -> bool:
        return name in self._symbols

    def declare(self, name: str, var_type: str, line: int, value) -> None:
        if self.is_declared(name):
            raise ValueError(
                f"Variable '{name}' ya declarada en línea "
                f"{self._symbols[name].declared_line}"
            )
        self._symbols[name] = SymbolInfo(name, var_type, line, value)
    
    def initialize_default(self, name: str):
        sym = self.get(name)
        if sym is not None and sym.value is None:
            sym.set_default()

    def get(self, name: str) -> Optional[SymbolInfo]:
        return self._symbols.get(name)

    def all_symbols(self) -> Dict[str, SymbolInfo]:
        return dict(self._symbols)
