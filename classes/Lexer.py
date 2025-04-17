from classes.Token import Token, TokenCategory
from data.TransitionMatrixes import identifier_matrix

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
            self.lines = file.readlines()  # Guardar líneas en self.lines
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
        value = ""
        # No incrementamos current_col_ix aquí, ya que lo hacemos en __read_char
        while self.current_col_ix + 1 < len(self.lines[self.current_row_ix]):
            self.current_col_ix += 1
            current_char = self.lines[self.current_row_ix][self.current_col_ix]
            if current_char.isalnum() or current_char == '_':
                value += current_char
            else:
                self.current_col_ix -= 1  # Retroceder para procesar el próximo carácter en __read_char
                break
        # Determinar si es un tipo de dato o un identificador
        category = TokenCategory.TYPE if value in ["Num", "Text", "Bool"] else TokenCategory.IDENTIFIER
        self.tokens.append(Token(category, value, self.current_row_ix + 1, self.current_col_ix - len(value) + 1))

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