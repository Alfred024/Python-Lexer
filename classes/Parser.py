from classes.Token import Token, TokenCategory

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos    = 0
        self.errors = []

    @property
    def look_ahead(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token(TokenCategory.EOF)

    def match(self, cat: TokenCategory):
        if self.look_ahead.category == cat:
            tok = self.look_ahead
            self.pos += 1
            return tok
        else:
            self.error(f"Se esperaba {cat}, se encontró {self.look_ahead.category}")
            return None

    def error(self, msg: str):
        self.errors.append(f"[Linea {self.look_ahead.row}] {msg}")
        # intentar recuperación mínima:
        self.pos += 1

    def parse_program(self):
        self.parse_lista_sentencias()
        self.match(TokenCategory.EOF)

    # ? Porqué aquí excluye cualquier cosa que no sea una KEYWORD o un IDENTIFIER? No sé si a lo mejor lo pusimos en las reglas de la gramática y se me está pasando ver eso, pero que yo sepa, si a un compilador le pasas un archivo que solo tenga un 10 por ejemplo, no marca error ni nada.
    def parse_lista_sentencias(self):
        # ListaSentencias → Sentencia ListaSentencias | ε
        while self.look_ahead.category in {
            TokenCategory.KEYWORD,       # Num, Text, Bool, If, While, For, Read, Write
            TokenCategory.IDENTIFIER,
        }:
            self.parse_sentencia()

    def parse_sentencia(self):
        cat = self.look_ahead.category
        val = self.look_ahead.value
        
        if cat == TokenCategory.KEYWORD and val in {"Num","Text","Bool"}:
            self.parse_declaracion()
        elif cat == TokenCategory.IDENTIFIER:
            self.parse_asignacion()
        elif cat == TokenCategory.KEYWORD and val == "If":
            self.parse_if()
        elif cat == TokenCategory.KEYWORD and val == "While":
            self.parse_while()
        elif cat == TokenCategory.KEYWORD and val == "For":
            self.parse_for()
        elif cat == TokenCategory.KEYWORD and val == "Read":
            self.parse_read()
        elif cat == TokenCategory.KEYWORD and val == "Write":
            self.parse_write()
        else:
            self.error(f"Sentencia inválida al inicio: {self.look_ahead}")

    def parse_declaracion(self):
        tipo = self.match(TokenCategory.KEYWORD)    # Num/Text/Bool
        ident= self.match(TokenCategory.IDENTIFIER)
        if self.look_ahead.category == TokenCategory.ASIG_OPER:
            self.match(TokenCategory.ASIG_OPER)
            self.parse_expresion()
        self.match(TokenCategory.DELIM_POINT)

    def parse_asignacion(self):
        ident = self.match(TokenCategory.IDENTIFIER)
        self.match(TokenCategory.ASIG_OPER)
        self.parse_expresion()
        self.match(TokenCategory.DELIM_POINT)

    def parse_if(self):
        self.match(TokenCategory.KEYWORD)           # If
        self.match(TokenCategory.DELIM_PARENT_LEFT) # '('
        self.parse_condicion()
        self.match(TokenCategory.DELIM_PARENT_RIGHT)
        self.match(TokenCategory.DELIM_BRACE_LEFT)  # '{'
        self.parse_lista_sentencias()
        self.match(TokenCategory.DELIM_BRACE_RIGHT) # '}'
        if self.look_ahead.category == TokenCategory.KEYWORD and self.look_ahead.value == "Else":
            self.match(TokenCategory.KEYWORD)
            self.match(TokenCategory.DELIM_BRACE_LEFT)
            self.parse_lista_sentencias()
            self.match(TokenCategory.DELIM_BRACE_RIGHT)

    def parse_while(self):
        self.match(TokenCategory.KEYWORD)  # While
        self.match(TokenCategory.DELIM_PARENT_LEFT)
        self.parse_condicion()
        self.match(TokenCategory.DELIM_PARENT_RIGHT)
        self.match(TokenCategory.DELIM_BRACE_LEFT)
        self.parse_lista_sentencias()
        self.match(TokenCategory.DELIM_BRACE_RIGHT)

    def parse_for(self):
        self.match(TokenCategory.KEYWORD)  # For
        self.match(TokenCategory.DELIM_PARENT_LEFT)
        # Asignación inicial
        if self.look_ahead.category == TokenCategory.IDENTIFIER:
            self.parse_asignacion()
        self.parse_condicion()
        self.match(TokenCategory.DELIM_POINT)
        self.parse_asignacion()
        self.match(TokenCategory.DELIM_PARENT_RIGHT)
        self.match(TokenCategory.DELIM_BRACE_LEFT)
        self.parse_lista_sentencias()
        self.match(TokenCategory.DELIM_BRACE_RIGHT)

    def parse_read(self):
        self.match(TokenCategory.KEYWORD)          # Read
        self.match(TokenCategory.DELIM_PARENT_LEFT)
        self.match(TokenCategory.IDENTIFIER)
        self.match(TokenCategory.DELIM_PARENT_RIGHT)
        self.match(TokenCategory.DELIM_POINT)

    def parse_write(self):
        self.match(TokenCategory.KEYWORD)          # Write
        self.match(TokenCategory.DELIM_PARENT_LEFT)
        self.parse_expresion()
        self.match(TokenCategory.DELIM_PARENT_RIGHT)
        self.match(TokenCategory.DELIM_POINT)

    def parse_condicion(self):
        self.parse_expresion()
        if self.look_ahead.category in {TokenCategory.REL_OPER, TokenCategory.LOG_OPER}:
            self.pos += 1  # consumir operador
            self.parse_expresion()

    def parse_expresion(self):
        self.parse_termino()
        while self.look_ahead.category in {TokenCategory.ARIT_OPER} and self.look_ahead.value in ['+','-']:
            self.pos += 1
            self.parse_termino()

    def parse_termino(self):
        self.parse_factor()
        while self.look_ahead.category in {TokenCategory.ARIT_OPER} and self.look_ahead.value in ['*','/']:
            self.pos += 1
            self.parse_factor()

    def parse_factor(self):
        if self.look_ahead.category == TokenCategory.NUM:
            self.pos += 1
        elif self.look_ahead.category == TokenCategory.IDENTIFIER:
            self.pos += 1
        elif self.look_ahead.category == TokenCategory.DELIM_PARENT_LEFT:
            self.match(TokenCategory.DELIM_PARENT_LEFT)
            self.parse_expresion()
            self.match(TokenCategory.DELIM_PARENT_RIGHT)
        else:
            self.error(f"Factor inválido: {self.look_ahead}")



parser = Parser(symtab.tokens)
parser.parse_program()

if parser.errors:
    print("Errores sintácticos:")
    for e in parser.errors:
        print(" ", e)
else:
    print("Análisis sintáctico exitoso.")
