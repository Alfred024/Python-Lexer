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
        ["(","Cond",")"],
        ["Exp","Oper_Cond","Exp"],
    ],
    "Oper_Cond": [
        ["REL_OPER"],
        ["LOG_OPER"]
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