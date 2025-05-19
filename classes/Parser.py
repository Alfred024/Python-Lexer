import data.grammatic as grammatic
from collections import defaultdict, deque
# from classes.SymbolTable import SymbolTable

EPSILON = "ε"
EOF = "$" # ! Este EOF se podría confundir con el inicio de un Token de tipo COMMENT

# Creación de terminakles y no terminales
# Manejo de set para no permitir elementos duplicados.
non_terminals = set(grammatic.grammar.keys())
terminals = set()
for rhss in grammatic.grammar.values():
    for right_hand_side in rhss:
        for sym in right_hand_side:
            if sym not in non_terminals and sym != EPSILON:
                terminals.add(sym)
terminals.add(EOF)
terminals.add(EPSILON)

print('non_terminals:')
print(non_terminals)
print('\n')
print('terminals:')
print(terminals)

# ───── 3) CÁLCULO DE FIRST y FOLLOW ─────────────────────────────────────
# Creación de un diccionario de datos 'valor': set()
FIRST = { X:set() for X in non_terminals } # Los primeros elementos terminales de la derivación de un no terminal
FOLLOW = { X:set() for X in non_terminals } #  Los primeros elementos terminales que aparecen inmediatamente después de un no terminal
# Inicializa FIRST para terminales
for t in terminals:
    FIRST[t] = {t}

# Obtiene los FIRST de la gramática
changed = True
while changed:
    changed = False
    for A, rhss in grammatic.grammar.items():
        for right_hand_side in rhss:
            # union FIRST(right_hand_side) \ {ε} en FIRST[A]
            first_rhs = set()
            nullable = True
            for sym in right_hand_side:
                # print(f'sym: {sym}')
                first_rhs |= (FIRST[sym] - {EPSILON})
                # print(f'first_rhs: {first_rhs}')
                if EPSILON not in FIRST[sym]:
                    nullable = False
                    break
            if nullable:
                first_rhs.add(EPSILON)
            if not first_rhs <= FIRST[A]:
                FIRST[A] |= first_rhs
                changed = True

# Obtiene los FOLLOW de la gramática
FOLLOW["Programa"].add(EOF)
changed = True
while changed:
    changed = False
    for A, rhss in grammatic.grammar.items():
        for right_hand_side in rhss:
            trailer = FOLLOW[A].copy()
            for sym in reversed(right_hand_side):
                if sym in non_terminals:
                    if not trailer <= FOLLOW[sym]:
                        FOLLOW[sym] |= trailer
                        changed = True
                    if EPSILON in FIRST[sym]:
                        trailer |= (FIRST[sym] - {EPSILON})
                    else:
                        trailer = FIRST[sym].copy()
                else:
                    trailer = FIRST[sym].copy()
                    
                    
print('\n')
print('FIRST: ')
print(FIRST)
print('\n')
print('FOLLOW: ')
print(FOLLOW)

# # ───── 4) CONSTRUIR TABLA LL(1) ───────────────────────────────────────────
# # tabla[(NoTerm, terminal)] = producción (lista de símbolos)
# parse_table = {}
# for A, rhss in grammatic.grammar.items():
#     for right_hand_side in rhss:
#         # FIRST(right_hand_side)
#         first_rhs = set()
#         nullable = True
#         for sym in right_hand_side:
#             first_rhs |= (FIRST[sym] - {EPSILON})
#             if EPSILON not in FIRST[sym]:
#                 nullable = False
#                 break
#         for t in first_rhs - {EPSILON}:
#             parse_table[(A,t)] = right_hand_side
#         if nullable:
#             for b in FOLLOW[A]:
#                 parse_table[(A,b)] = right_hand_side

# # ───── 5) PARSER PREDICTIVO DIRIGIDO POR TABLA ────────────────────────────
# class TableParser:
#     def __init__(self, tokens: list[Token], symtab: SymbolTable):
#         # tokens deben terminar con un EOF token
#         self.tokens = tokens
#         self.symtab = symtab
#         self.stack  = deque()
#         self.stack.append(EOF)
#         self.stack.append("Programa")
#         self.pos = 0

#     @property
#     def la(self) -> Token:
#         return self.tokens[self.pos]

#     def error(self, msg):
#         raise SyntaxError(f"[Linea {self.la.row}] {msg}")

#     def parse(self):
#         while self.stack:
#             top = self.stack.pop()
#             look = self.la

#             # 1) Acción semántica integrada
#             #    (no la usamos aquí; podrías insertar callables en la RHS)

#             # 2) Si es terminal:
#             if top in terminals:
#                 # Comparar literal vs categorías
#                 if ((top == look.category.name) or
#                     (top == look.value) or
#                     (top == EOF and look.category==TokenCategory.EOF)):
#                     self.pos += 1
#                 else:
#                     self.error(f"Se esperaba '{top}', se encontró '{look.value}'")
#             # 3) Si es no-terminal:
#             elif top in non_terminals:
#                 key = (top, look.value) if (top, look.value) in parse_table else (top, look.category.name)
#                 prod = parse_table.get(key)
#                 if not prod:
#                     self.error(f"No hay producción para ({top}, {look.value})")
#                 # Push en orden inverso, omitiendo ε
#                 for sym in reversed(prod):
#                     if sym != EPSILON:
#                         self.stack.append(sym)
#             else:
#                 self.error(f"Símbolo desconocido en pila: {top}")

#         # Al final, si consumimos todo
#         if self.la.category != TokenCategory.EOF:
#             self.error("Tokens sobrantes tras parsear")

#         return True