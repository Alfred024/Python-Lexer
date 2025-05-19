EPSILON = "ε"
EOF = "$" # ! Este EOF se podría confundir con el inicio de un Token de tipo COMMENT

# GRAMÁTICA (NoTerminal → lista de RHS)
grammar = {
    "Programa": [["ListaSentencias"]],
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