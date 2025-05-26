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
        ["Num", "IDENTIFIER", ".",],
        ["Text", "IDENTIFIER", ".",],        
        ["Bool","IDENTIFIER","."],
        
        ["Num","IDENTIFIER","=", "Exp","."],
        ["Text","IDENTIFIER","=", "Exp","."],
        ["Bool","IDENTIFIER","=","Exp","."],
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
        ["For","(","Asignacion","Cond",".","Asignacion",")","{","ListaSentencias","}"],
        ["For","(","Declaracion","Cond",".","Asignacion",")","{","ListaSentencias","}"],
    ],
    "ReadSent": [["Read","(","IDENTIFIER",")","."]],
    "WriteSent": [["Write","(","Exp",")","."]],
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
    "Term": [["Factor","Term'"]],
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