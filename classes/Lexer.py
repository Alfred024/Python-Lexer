from classes.Token import Token, TokenCategory
import data.TransitionMatrixes.identifier_matrix as id_matrix

class Lexer:
    def __init__(self, file_input: str):
        self.dictionary = {
            'delim_chars': ['(', ')', '{', '}', '.'],
            'oper_chars': ['+', '-', '*', '/', '=', '<', '>', '&', '|', '!'],
            'spaces': ['\n', '\t', ' '],  # Corregido: '' no es un espacio válido
        }
        self.tokens: list[Token] = []
        self.file_input = file_input
        self.current_row_ix = 0
        self.current_col_ix = 0
        self.lines = []  # Almacenar las líneas del archivo
        self.__read_input()

    def __read_input(self):
        # Leer el archivo y almacenar las líneas
        with open(self.file_input, 'r') as file:
            self.lines = [line.strip() for line in file.readlines()]  # Guardar líneas en self.lines
        self.current_row_ix = 0
        # Procesar cada línea y carácter
        while self.current_row_ix < len(self.lines):
            self.current_col_ix = 0
            while self.current_col_ix < len(self.lines[self.current_row_ix]):
                char = self.lines[self.current_row_ix][self.current_col_ix]
                self.__read_char(char)
                self.current_col_ix += 1
            self.current_row_ix += 1

    def __read_char(self, char: str):
        if char == '@':
            self.__read_identifier()
        elif char == '$':
            # TODO: Enviar a matriz de comentarios
            pass
        elif char in self.dictionary['delim_chars']:
            self.tokens.append(Token(TokenCategory.DELIMITER, char, self.current_row_ix + 1, self.current_col_ix + 1))
        elif char in self.dictionary['oper_chars']:
            self.tokens.append(Token(TokenCategory.OPERATOR, char, self.current_row_ix + 1, self.current_col_ix + 1))
        elif char in self.dictionary['spaces']:
            # Ignorar espacios en blanco
            pass
        else:
            # TODO: Manejar otros caracteres (números, palabras, etc.)
            pass

    def __read_identifier(self):
        value = "@" # Iniciamos con el carácter @, que ya habiamos detectado
        state = 0 # Empezamos desde el estado inicial de la matriz de transicion 
        
        if '@' in id_matrix.identifier_matrix[state]:
            state = id_matrix.identifier_matrix[state]['@']
        else:
            print(f"Error: No transición válida para '@' en estado 0")
            return
        
        while self.current_col_ix + 1 < len(self.lines[self.current_row_ix]):
            self.current_col_ix += 1 
            char = self.lines[self.current_row_ix][self.current_col_ix]
            #print(f"DEBUG: char='{char}' | state={state} | value={value}")

            # Transición válida segun la matriz
            if state in id_matrix.identifier_matrix and char in id_matrix.identifier_matrix[state]:
               state = id_matrix.identifier_matrix[state][char] # Cambiamos al nuevo estado
               value += char  # Agregamos el carácter al nombre del identificador 
            elif state == 2 and char == '.': # Si estamos en estado 2 y encontramos un punto significa que termino
                value += char
                break  
            else: # Aqui es un estado de error 
                state = -1
                break
        if state == 2 and value.endswith('.'): #Aqui se hace una validacion final con el punto ya que no esta en la matriz
            value = value[:-1] # Se quieta el punto para guardar solo el nombre real del identificador
            ident_name = value[1:] #Se quita el @ para guardar solo el nombre y asi pase bien por el filtro de las palabras reservadas ya que habia un error y siempre validaba las palabras reservadas
            if len(ident_name) > 15: #Valisdacion de longitud 
                print(f"Error: Identificador demasiado largo '{value}'")
                return
            if ident_name in ["While", "For", "If", "Else", "Read", "Write", "Num", "Text", "Bool", "True", "False"]: #validar palabras reservadas
                print(f"Error: '{value}' es una palabra reservada")
                return
            self.tokens.append(Token( #Si todo esta bien lo guardamos en el token 
                TokenCategory.IDENTIFIER,
                value,
                self.current_row_ix + 1,
                self.current_col_ix - len(value) + 2 
            ))
            print(f"Token IDENTIFIER válido: '{value}' en línea {self.current_row_ix + 1}")


        else:
           print(f"Error: Identificador mal formado en línea {self.current_row_ix + 1}, columna {self.current_col_ix + 1}")


    def __read_comment(self) -> Token:
        pass

    def __read_word(self) -> Token:
        pass

    def __read_number(self) -> Token:
        pass

    def __read_delimitator(self) -> Token:
        pass

    def __read_operator(self) -> Token:
        pass

    def __is_whitespace(self) -> bool:
        pass

    def __error_char_index(self) -> int:
        pass