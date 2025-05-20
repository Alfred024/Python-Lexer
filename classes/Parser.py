# import data.grammatic as grammatic
# from classes.Token import Token, TokenCategory
# from classes.SymbolTable import SymbolTable
from collections import defaultdict, deque

EPSILON = "ε"
EOF = "$" # ! Este EOF se podría confundir con el inicio de un Token de tipo COMMENT

# GRAMÁTICA (NoTerminal → lista de RHS)
grammar = {
    "Programa": [
        ["ListaSentencias"]
    ],
    "ListaSentencias": [
        ["Sentencia", "ListaSentencias"],
        [EPSILON]
    ],
    "Sentencia": [
        ["Declaracion"],
        ["Asignacion"],
        ["IfSent"],
        ["WhileSent"],
        ["ForSent"],
        ["ReadSent"],
        ["WriteSent"]
    ],
    "Declaracion": [
        ["Num", "IDENTIFIER", ".",],
        ["Text", "IDENTIFIER", ".",],        
        ["Bool","IDENTIFIER","."],
        
        ["Num","IDENTIFIER","=", "Exp","."],
        ["Text","IDENTIFIER","=", "Exp","."],
        ["Bool","IDENTIFIER","=","Exp","."]
    ],
    "Asignacion": [
        ["IDENTIFIER","=","Exp","."]
    ],
    "IfSent": [
        ["If","(","Cond",")","{","ListaSentencias","}"],
        ["If","(","Cond",")","{","ListaSentencias","}","Else","{","ListaSentencias","}"],
    ],
    "WhileSent": [
        ["While","(","Cond",")","{","ListaSentencias","}"]
    ],
    "ForSent": [
        ["For","(","Asignacion","Cond",".","Asignacion",")","{","ListaSentencias","}"]
    ],
    "ReadSent": [["Read","(","IDENTIFIER",")","."]],
    "WriteSent": [["Write","(","Exp",")","."]],
    "Cond": [
        ["Exp","REL_OPER","Exp"],
        ["Exp","LOG_OPER","Exp"],
        ["(","Cond",")"]
    ],
    "Exp": [
        ["Term","Exp'"]
    ],
    "Exp'": [
        ["ARIT_OPER","+","Term","Exp'"],
        ["ARIT_OPER","-","Term","Exp'"],
        [EPSILON]
    ],
    "Term": [["Factor","Term'"]],
    "Term'": [
        ["ARIT_OPER","*","Factor","Term'"],
        ["ARIT_OPER","/","Factor","Term'"],
        [EPSILON]
    ],
    "Factor":[
        ["IDENTIFIER"],
        ["NUM"],
        ["(","Exp",")"]
    ],
}

# Creación de terminakles y no terminales
# Manejo de set para no permitir elementos duplicados.
non_terminals = set(grammar.keys())
terminals = set()
for rhss in grammar.values():
    for right_hand_side in rhss:
        for sym in right_hand_side:
            if sym not in non_terminals and sym != EPSILON:
                terminals.add(sym)
terminals.add(EOF)
terminals.add(EPSILON)

# print('non_terminals:')
# print(non_terminals)
# print('\n')
# print('terminals:')
# print(terminals)

# CÁLCULO DE FIRST y FOLLOW ─────────────────────────────────────
FIRST = { element : set() for element in non_terminals } # Los primeros elementos terminales de la derivación de un no terminal les establecerá en en 0 primero
# Cuando (A) es un terminal, el FIRST de este será el mismo
for terminal in terminals:
    FIRST[terminal] = { terminal }
print('FIRST')
print(FIRST)

# Obtiene los FIRST de la gramática
changed = True
while changed:
    changed = False

    for A, rhss in grammar.items():
        # Itera sobre todas las producciones de una gramática
        print(f'A: {A}')
        for rhs in rhss:
            print(F'RHS de {A} --> {rhs}')
            first_rhs = set()
            nullable = True
            for sym in rhs:
                print(f'Symb de RHS: {sym}')
                
                # Obtiene todos los terminales de un 
                for terminal in FIRST[sym]:
                    print(f'TERM de {sym}: {terminal}')
                    # Si el terminal no es EPSILON, agrega a
                    if terminal != EPSILON:
                        first_rhs.add(terminal)

                # Ese símbolo no puede ser nullable, por lo que deja de buscar en esa rhs un símbolo 
                if EPSILON not in FIRST[sym]:
                    nullable = False
                    break
             
            if nullable:
                first_rhs.add(EPSILON)
            
            added_any = False
            for terminal in first_rhs:
                if terminal not in FIRST[A]:
                    print(f'Voy a aagrergar {terminal} al elemento {A}')
                    FIRST[A].add(terminal)
                    # print(FIRST)
                    added_any = True
            
            if added_any:
                changed = True
        print('--------------------------------')

print('FIRST FINAL: ')
print(FIRST)
FOLLOW = { X:set() for X in non_terminals }
FOLLOW["Programa"].add(EOF)
changed = True
while changed:
    changed = False

    for A, rhss in grammar.items():
        for rhs in rhss:
            trailer = []
            for sym in FOLLOW[A]:
                trailer.append(sym)

            for sym in reversed(rhs):
                if sym in non_terminals:
                    for terminal in trailer:
                        if terminal not in FOLLOW[sym]:
                            FOLLOW[sym].add(terminal)
                            changed = True

                    new_trailer = []
                    for t in FIRST[sym]:
                        if t != EPSILON and t not in new_trailer:
                            new_trailer.append(t)

                    if EPSILON in FIRST[sym]:
                        for t in trailer:
                            if t not in new_trailer:
                                new_trailer.append(t)

                    trailer = new_trailer

                else:
                    trailer = [sym]
                    

print('\n')
print('FIRST: ')              
print(FIRST)
print('\n')
print('FOLLOW: ')
print(FOLLOW)

# # ───── 4) CONSTRUIR TABLA LL(1) ───────────────────────────────────────────
# # tabla[(NoTerm, terminal)] = producción (lista de símbolos)
# parse_table = {}
# for A, rhss in grammar.items():
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

# print('\nparse_table: ')
# print(parse_table)

# class TableParser:
#     def __init__(self, tokens, symtab):
#         # tokens deben terminar con un EOF token
#         self.tokens = tokens
#         self.symtab = symtab
#         self.stack  = deque()
#         self.stack.append(EOF)
#         self.stack.append("Programa")
#         self.pos = 0

#     @property
#     def look_ahead(self):
#         return self.tokens[self.pos]

#     def parse(self):
#         # TODO: Hacer el código de parseo que consuma self.stack
#         pass