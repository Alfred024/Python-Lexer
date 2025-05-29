# GRAMÁTICA (NoTerminal → lista de RHS)
EPSILON = "ε"
EOF = "#" # ! Este EOF se podría confundir con el inicio de un Token de tipo COMMENT

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
        ["Num", "IDENTIFIER", "DeclaracionDeriv"],
        ["Text", "IDENTIFIER", "DeclaracionDeriv"],
        ["Bool", "IDENTIFIER", "DeclaracionDeriv"],
    ],
    "DeclaracionDeriv": [
        ["."] ,
        ["=", "Exp", "."],
    ],
    "Asignacion": [
        ["IDENTIFIER","=","Exp","."]
    ],
    "IfSent": [
        ["If","(","Cond",")","{","ListaSentencias","}", "IfElse"],
    ],
    "IfElse": [
        ["Else","{","ListaSentencias","}"],
        [EPSILON]
    ],
    "WhileSent": [
        ["While","(","Cond",")","{","ListaSentencias","}"]
    ],
    "ForSent": [
        ["For","(","ForInit","Cond",".","Asignacion",")","{","ListaSentencias","}"],
    ],
    "ForInit": [
        ["Declaracion"],
        ["Asignacion"],
    ],
    "ReadSent": [
        ["Read","(","IDENTIFIER",")","."]
    ],
    "WriteSent": [
        ["Write","(","Exp",")","."]
    ],
    "Cond": [
        ["RelExpr", "CondPrime"],
        ["(", "Cond", ")", "CondPrime"],
    ],
    "CondPrime": [
        ["LOG_OPER", "Cond"],
        [EPSILON]
    ],
    "RelExpr": [
        ["Exp", "REL_OPER", "Exp"],
    ],
    "Exp": [
        ["Term","Exp'"]
    ],
    "Exp'": [
        ["+", "Term", "Exp'"],
        ["-", "Term", "Exp'"],
        [EPSILON]
    ],
    "Term": [
        ["Factor","Term'"]
    ],
    "Term'": [
        ["*","Factor","Term'"],
        ["/","Factor","Term'"],
        [EPSILON]
    ],
    "Factor":[
        ["IDENTIFIER"],
        ["NUM"],
        ["TEXT"],
        ["BOOL"],
        ["(","Exp",")"]
    ],
}

# Si la gramática es un factor y el sigueinte token es un operador aritmético, debe de comprobar que el sigueinte token sea de la misma categoría. 
    # Si es identifier, busca la categoría en la tabla de símbolos,
    # Si no es identifier, busca la categoría directamente