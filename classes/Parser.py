# import data.grammatic as grammatic
from data.grammatic import grammar, EOF, EPSILON
from collections import deque
from classes.Token import Token, TokenCategory
from classes.SymbolTable import SymbolTable

class TableParser:
    def __init__(self, tokens: list[Token], symtab: SymbolTable):
        self.sync_cats = { TokenCategory.DELIM_BRACE_RIGHT, TokenCategory.DELIM_PARENT_RIGHT, TokenCategory.DELIM_POINT }
        self.tokens = tokens + [ Token(TokenCategory.EOF, value=EOF, row=-1, column=-1) ]
        self.symtab = symtab
        self.stack  = deque()
        self.stack.append(EOF)
        self.stack.append("ListaSentencias")
        self.stack.append("Programa")
        self.pos = 0
        self._last_declared: str = ""
        
        self.terminals = set()
        self.non_terminals = set()
        self.parse_table = {}
        self.first = None
        self.follow = None
        
        # Setts the initial structures to create a parser
        self.__set_no_terminals()
        self.__set_terminals()
        self.__create_first()
        self.__create_follow()
        self.__create_parse_table()

    @property
    def look_ahead(self) -> Token:
        return self.tokens[self.pos]

    def __panic(self, msg: str):
        # 1) Reportar
        print(f"[Sintactic error:] {msg} (row {self.look_ahead.row})")
        # 2) Descarta hasta hallar uno de los sync_cats o EOF
        while (self.pos < len(self.tokens)
               and self.look_ahead.category not in self.sync_cats
               and self.look_ahead.category != TokenCategory.EOF):
            self.pos += 1
        # 3) Consume ese token de sincronización (si no es EOF)
        if (self.pos < len(self.tokens)
            and self.look_ahead.category in self.sync_cats):
            self.pos += 1
        # 4) Evita desbordarte
        if self.pos >= len(self.tokens):
            self.pos = len(self.tokens) - 1
        # 5) Resetea la pila hasta ListaSentencias
        while self.stack and self.stack[-1] != "ListaSentencias":
            self.stack.pop()
        # Al volver al parse(), reexpandir ListaSentencias
        return

    def parse(self):
        while self.stack:
            # Si ya llegamos al EOF real, éxito
            if self.look_ahead.category == TokenCategory.EOF:
                return True

            top = self.stack.pop()
            tok = self.look_ahead

            # Caso 1: EOF en pila → fin exitoso
            if top == EOF:
                return True

            # CASO A: terminal
            if top in self.terminals:
                if (top == tok.value) or (top == tok.category.name):
                    if tok.category == TokenCategory.IDENTIFIER:
                        if not self.symtab.is_declared(tok.value):
                            print(f"[Semantic error:] Variable '{tok.value}' no declarada (row {tok.row})")
                            # recover con panic
                            self.__panic(f"Esperaba IDENTIFIER declarado, vino '{tok.value}'")
                    self.pos += 1
                else:
                    self.__panic(f"Waiting for '{top}', but '{tok.value}' founded instead")
                continue

            # CASO B: no-terminal
            if top in self.non_terminals:
                key = (top, tok.value) if (top, tok.value) in self.parse_table else (top, tok.category.name)
                prod = self.parse_table.get(key)

                if prod is None:
                    # si es nullable, lo omitimos
                    if "#" in self.first[top]:  # aquí EPSILON
                        continue
                    self.__panic(f"No production found for ({top}, {tok.value})")
                    continue

                # === ACCIONES SEMÁNTICAS PARA DECLARACIÓN ===
                if top == "Declaracion":
                    # esperamos: [Tipo, IDENTIFIER, DeclaracionDeriv]
                    tipo_tok = self.tokens[self.pos]       # Num|Text|Bool
                    ident_tok = self.tokens[self.pos + 1]  # IDENTIFIER
                    name = ident_tok.value
                    vtype = tipo_tok.value
                    try:
                        self.symtab.declare(name, vtype, ident_tok.row)
                        self._last_declared = name
                    except ValueError:
                        print(f"[Semantic error:] Variable '{name}' ya declarada (row {ident_tok.row})")
                        # panic y continuar
                        self.__panic(f"Redeclaration of '{name}'")
                        # no hacemos push de la producción
                        continue

                # empujar RHS en orden inverso (omitimos ε)
                for s in reversed(prod):
                    if s != EPSILON:  # EPSILON
                        self.stack.append(s)

                continue

            # CASO C: símbolo inválido en pila
            self.__panic(f"Unknown symbol on stack: {top}")
        return True
    
    def __set_no_terminals(self):
        self.non_terminals = set(grammar.keys())
    
    def __set_terminals(self):
        for rhs_statements in grammar.values():
            for right_hand_side in rhs_statements:
                for sym in right_hand_side:
                    if sym not in self.non_terminals and sym != EPSILON:
                        self.terminals.add(sym)
        
        self.terminals.add(EOF)
        self.terminals.add(EPSILON)

    def __create_first(self):
        # Set elements as empty to non_terminals
        self.first = { element : set() for element in self.non_terminals } 
        # Set first of a terminal as its own
        for terminal in self.terminals:
            self.first[terminal] = { terminal }
        
        changed = True  # Var to handle if the exploration in grammatic keep founding new productions
        while changed:
            changed = False
            for A, rhs_statements in grammar.items():
                for rhs in rhs_statements:
                    # print(F'RHS de {A} --> {rhs}')
                    first_rhs = set()
                    nullable = True
                    for sym in rhs:
                        
                        for term in self.first[sym]:
                            if term != EPSILON:
                                first_rhs.add(term)

                        # Ese símbolo no puede ser nullable, por lo que deja de buscar en esa rhs un símbolo 
                        if EPSILON not in self.first[sym]:
                            nullable = False
                            break
                    
                    if nullable:
                        first_rhs.add(EPSILON)
                    
                    added_any = False
                    for term in first_rhs:
                        # Add first´s values founded 
                        if term not in self.first[A]:
                            self.first[A].add(term)
                            added_any = True
                    
                    if added_any:
                        changed = True

    def __create_follow(self):
        self.follow = { element :set() for element in self.non_terminals }
        self.follow["Programa"].add(EOF)
        
        changed = True
        while changed:
            changed = False

            for A, rhs_statements in grammar.items():
                for rhs in rhs_statements:
                    trailer = []
                    for sym in self.follow[A]:
                        trailer.append(sym)

                    for sym in reversed(rhs):
                        if sym in self.non_terminals:
                            for term in trailer:
                                if term not in self.follow[sym]:
                                    self.follow[sym].add(term)
                                    changed = True

                            new_trailer = []
                            for t in self.first[sym]:
                                if t != EPSILON and t not in new_trailer:
                                    new_trailer.append(t)

                            if EPSILON in self.first[sym]:
                                for t in trailer:
                                    if t not in new_trailer:
                                        new_trailer.append(t)

                            trailer = new_trailer

                        else:
                            trailer = [sym]

    def __create_parse_table(self):
        for nonterm, productions in grammar.items():
            for rhs in productions:
                first_rhs = set()
                nullable = True

                for sym in rhs:
                    # Añadimos todos los terminales de self.first[sym] excepto ε
                    for tok in self.first[sym]:
                        if tok != EPSILON and tok not in first_rhs:
                            first_rhs.add(tok)

                    # Si sym NO puede producir ε, la cadena ya no es nullable
                    if EPSILON not in self.first[sym]:
                        nullable = False
                        break

                # Si todos los símbolos podían producir ε, marcamos RHS como nullable
                if nullable:
                    first_rhs.add(EPSILON)

                # 2) Para cada terminal t en self.first(rhs) distinto de ε,
                #    ponemos la producción en la celda (nonterm, t)
                for t in first_rhs:
                    if t == EPSILON:
                        continue
                    key = (nonterm, t)
                    self.parse_table[key] = rhs

                # 3) Si RHS es nullable, también se aplica para cada b en self.follow[A]
                if nullable:
                    for b in self.follow[nonterm]:
                        key = (nonterm, b)
                        self.parse_table[key] = rhs