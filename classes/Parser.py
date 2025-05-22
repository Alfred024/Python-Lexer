# import data.grammatic as grammatic
from data.grammatic import grammar, EOF, EPSILON
from collections import deque
from classes.Token import Token, TokenCategory
from classes.SymbolTable import SymbolTable

# Creación de terminakles y no terminales
# Manejo de set para no permitir elementos duplicados.
class TableParser:
    def __init__(self, tokens: list[Token], symtab: SymbolTable):
        # self.tokens = tokens + [ Token(TokenCategory.EOF, value=EOF, row=-1, column=-1) ]
        self.tokens = tokens
        self.symtab = symtab
        self.stack  = deque()
        self.stack.append(EOF)
        self.stack.append("ListaSentencias")
        self.stack.append("Programa")
        self.pos = 0
        
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

    def error(self, msg):
        raise SyntaxError(f"[Linea {self.look_ahead.row}] {msg}")

    def parse(self):
        while self.stack:
            top = self.stack.pop()
            look = self.look_ahead
            print(f'Top: {top}')
            print(f'Look: {look}')
            # 1) Acción semántica integrada
            #    (no la usamos aquí; podrías insertar callables en la RHS)

            # 2) Si es terminal:
            if top in self.terminals:
                # Comparar literal vs categorías
                if ((top == look.category.name) or
                    (top == look.value) or
                    (top == EOF and look.category==TokenCategory.EOF)):
                    self.pos += 1
                else:
                    self.error(f"Se esperaba '{top}', se encontró '{look.value}'")
            # 3) Si es no-terminal:
            elif top in self.non_terminals:
                key = (top, look.value) if (top, look.value) in self.parse_table else (top, look.category.name)
                prod = self.parse_table.get(key)
                if not prod:
                    self.error(f"No hay producción para ({top}, {look.value})")
                # Push en orden inverso, omitiendo ε
                for sym in reversed(prod):
                    if sym != EPSILON:
                        self.stack.append(sym)
            else:
                self.error(f"Símbolo desconocido en pila: {top}")

        # Al final, si consumimos todo
        if self.look_ahead.category != TokenCategory.EOF:
            self.error("Tokens sobrantes tras parsear")

        return True
    
    def __set_no_terminals(self):
        self.non_terminals = set(grammar.keys())
        print(f'self.non_terminals: \n{self.non_terminals}\n')
    
    def __set_terminals(self):
        for rhss in grammar.values():
            for right_hand_side in rhss:
                for sym in right_hand_side:
                    if sym not in self.non_terminals and sym != EPSILON:
                        self.terminals.add(sym)
        
        self.terminals.add(EOF)
        self.terminals.add(EPSILON)
        print(f'self.terminals: \n{self.terminals}\n')

    def __create_first(self):
        self.first = { element : set() for element in self.non_terminals } # Los primeros elementos terminales de la derivación de un no terminal les establecerá en en 0 primero
        # Cuando (A) es un terminal, el self.first de este será el mismo
        for terminal in self.terminals:
            self.first[terminal] = { terminal }
        
        changed = True
        while changed:
            changed = False

            for A, rhss in grammar.items():
                # Itera sobre todas las producciones de una gramática
                # print(f'A: {A}')
                for rhs in rhss:
                    # print(F'RHS de {A} --> {rhs}')
                    first_rhs = set()
                    nullable = True
                    for sym in rhs:
                        # print(f'Symb de RHS: {sym}')
                        
                        for terminal in self.first[sym]:
                            # print(f'TERM de {sym}: {terminal}')
                            # Si el terminal no es EPSILON, agrega a
                            if terminal != EPSILON:
                                first_rhs.add(terminal)

                        # Ese símbolo no puede ser nullable, por lo que deja de buscar en esa rhs un símbolo 
                        if EPSILON not in self.first[sym]:
                            nullable = False
                            break
                    
                    if nullable:
                        first_rhs.add(EPSILON)
                    
                    added_any = False
                    for terminal in first_rhs:
                        if terminal not in self.first[A]:
                            # print(f'Voy a agregar {terminal} al elemento {A}')
                            self.first[A].add(terminal)
                            # print(self.first)
                            added_any = True
                    
                    if added_any:
                        changed = True

        print(f'self.first: \n{self.first}\n')

    def __create_follow(self):
        self.follow = { X:set() for X in self.non_terminals }
        self.follow["Programa"].add(EOF)
        
        changed = True
        while changed:
            changed = False

            for A, rhss in grammar.items():
                for rhs in rhss:
                    trailer = []
                    for sym in self.follow[A]:
                        trailer.append(sym)

                    for sym in reversed(rhs):
                        if sym in self.non_terminals:
                            for terminal in trailer:
                                if terminal not in self.follow[sym]:
                                    self.follow[sym].add(terminal)
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
                            
        print(f'self.follow: \n{self.follow}\n')

    def __create_parse_table(self):
        for nonterm, productions in grammar.items():
            # Para cada regla A → RHS_list
            for rhs in productions:
                # 1) Calcular self.first(rhs) de forma explícita
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
                    # (Opcional) puedes avisar si sobrescribes una entrada:
                    # if key in self.parse_table:
                    #     print(f"Warning: M[{nonterm},{t}] ya estaba definido")
                    self.parse_table[key] = rhs

                # 3) Si RHS es nullable, también se aplica para cada b en self.follow[A]
                if nullable:
                    for b in self.follow[nonterm]:
                        key = (nonterm, b)
                        # if key in self.parse_table:
                        #     print(f"Warning: M[{nonterm},{b}] ya estaba definido por ε-producción")
                        self.parse_table[key] = rhs
                        
        print(f'PARSE TABLE: \n{self.parse_table}\n')