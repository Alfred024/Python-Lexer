
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
                for char in row:
                    # TODO: Llevar el índice de los caracteres en la fila actual
                    self.__read_char(char)
                            
    def __read_char(self, char : str):
        if(char == '@'):
            # enviar a matriz identificador
            pass
        elif(char == '$'):
            # enviar a matriz comentario
            pass
    
    def __read_identifier() -> Token:
        pass
    
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
    
    def __get_next_token():
        pass
    
    def __is_whitespace() -> bool:
        pass
    
    def __error_char_index() -> int:
        pass
    
print(identifier_matrix)