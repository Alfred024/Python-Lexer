# classes/symbol_table.py
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional


class SymbolKind(Enum):
    VARIABLE   = auto()
    CONSTANT   = auto()
    FUNCTION   = auto()
    PARAMETER  = auto()
    KEYWORD    = auto()     # por si quieres registrar palabras reservadas


@dataclass
class SymbolInfo:
    lexeme: str
    kind: SymbolKind
    data_type: str          # "Num", "Text", "Bool", etc.
    line: int
    column: int
    scope_level: int        # 0 = global, 1 = dentro de la 1.ª función, ...
    extra: dict = field(default_factory=dict)   # para lo que necesites (valor, tamaño, etc.)

    def __repr__(self):
        return (f"<{self.lexeme}:{self.data_type} "
                f"{self.kind.name} L{self.line} C{self.column} S{self.scope_level}>")


class SymbolTable:
    """Tabla de símbolos con manejo de scopes anidados."""
    
    def __init__(self):
        # Una pila de diccionarios: cada dicc es un scope
        self._scopes: List[Dict[str, SymbolInfo]] = [{}]  # scope 0 = global

    # ---------- ÁMBITOS ----------
    @property
    def current_level(self) -> int:
        return len(self._scopes) - 1

    def enter_scope(self) -> None:
        """Abre un nuevo ámbito."""
        self._scopes.append({})

    def exit_scope(self) -> None:
        """Sale del ámbito actual."""
        if len(self._scopes) == 1:
            raise RuntimeError("No se puede salir del scope global")
        self._scopes.pop()

    # ---------- CRUD ----------
    def add(self, lexeme: str, kind: SymbolKind, data_type: str,
            line: int, column: int, **extra) -> SymbolInfo:
        """Inserta un símbolo en el scope actual; error si ya existe ahí."""
        scope = self._scopes[-1]
        if lexeme in scope:
            raise ValueError(f"Símbolo redeclarado: '{lexeme}' en L{line} C{column}")
        info = SymbolInfo(
            lexeme=lexeme,
            kind=kind,
            data_type=data_type,
            line=line,
            column=column,
            scope_level=self.current_level,
            extra=extra
        )
        scope[lexeme] = info
        return info

    def lookup(self, lexeme: str) -> Optional[SymbolInfo]:
        """Busca desde el ámbito actual hacia arriba. Devuelve None si no existe."""
        for scope in reversed(self._scopes):
            if lexeme in scope:
                return scope[lexeme]
        return None

    def exists_in_current(self, lexeme: str) -> bool:
        return lexeme in self._scopes[-1]

    # ---------- Depuración ----------
    def dump(self) -> None:
        for lvl, scope in enumerate(self._scopes):
            print(f"\nScope {lvl}:")
            for sym in scope.values():
                print("  ", sym)
