
from classes.Token import Token, TokenCategory
from data.TransitionMatrixes import identifier_matrix

class Lexer:
    
    def __init__(self, file_input : str):
        self.dictionary = {
            'delim_chars': [ '(', ')', '{', '}', '.' ],
            'oper_chars': [ '+', '-', '*', '/', '=', '<', '>', '&', '|', '!' ],
            'spaces': [ '\n', '\t', '' ],
        }
        self.tokens : list[Token] = []
        self.file_input = file_input
        self.__read_input()
        self.current_row_ix =  0
        self.current_col_ix =  0

    def __read_input(self):
        # Open file in read mode
        with open(self.file_input, 'r') as file:
            for row in file:
                self.current_row_ix += 1
                for char in row:
                    self.__read_char(char)
                            
    def __read_char(self, char : str):
        if(char == '@'):
            self.__read_identifier()
        elif(char == '$'):
            # enviar a matriz comentario
            pass
        elif(char in self.dictionary['delim_chars']):
            # enviar a matriz delimitadores
            pass
        elif(char in self.dictionary['oper_chars']):
            # enviar a matriz operadores
            pass
        elif(char in self.dictionary['spaces']):
            # enviar a matriz espacios
            pass
    
    def __read_identifier(self):
        value = ""
        self.current_col_ix += 1  # Aqui ignoramos el @ ya que sabemos que es un identificador y no es neceasrio evaluarlo de nuevo
        while self.current_col_ix < len(self.lines[self.current_row_ix]):
            current_char = self.lines[self.current_row_ix][self.current_col_ix]
            if current_char.isalnum() or current_char == '_':  # Revisamos si el caracter actual es alfanumérico o un guion bajo
                value += current_char # En caso de que sea valido de almacena en la variable
                self.current_col_ix += 1
            else:
                break
        self.tokens.append(Token("IDENTIFIER", value)) #Creamos el nuevo token con el valor que almacenamos anteriormente
        
    def __read_comment() -> Token:
        pass
    def __read_word() -> Token:
        pass
    def __read_number() -> Token:
        pass
    def __read_delimitator() -> Token:
        pass
    def __read_operator() -> Token:
        pass
    
    def __is_whitespace() -> bool:
        pass
    def __error_char_index() -> int:
        pass
    
print(identifier_matrix)