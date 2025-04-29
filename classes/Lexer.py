# Classes
from classes.Token import Token, TokenCategory
# Dictionary 📑
import data.dictionary as dictionary
# Transition matrixes 
    # Identifiers matrix
from data.TransitionMatrixes.identifier_matrix import IdentifierStates
import data.TransitionMatrixes.identifier_matrix as id_matrix
    # Delims matrix
# Comments matrix
from data.TransitionMatrixes.comment_matrix import CommentStates
import data.TransitionMatrixes.comment_matrix as comment_matrix
# Keywords matrix
from data.TransitionMatrixes.keyword_matrix import KeywordStates
import data.TransitionMatrixes.keyword_matrix as keyword_matrix

class Lexer:
    def __init__(self, file_input: str):
        self.tokens: list[Token] = []
        self.file_input = file_input
        self.current_row_ix = 0
        self.current_col_ix = 0
        self.row_list = []
        self.keywords = ["While", "For", "If", "Else", "Read", "Write", "Num", "Text", "Bool", "True", "False"]
        self.__read_input()

    def __read_input(self):
        # Get rows of the file
        with open(self.file_input, 'r') as file:
            self.row_list = [line.strip() for line in file.readlines()]

        # Read every char from file_input
        self.current_col_ix = 0
        while self.current_row_ix < len(self.row_list):
            self.current_col_ix = 0
            while self.current_col_ix < len(self.row_list[self.current_row_ix]):
                char = self.row_list[self.current_row_ix][self.current_col_ix]
                self.__categorize_char(char)
                self.current_col_ix += 1
            self.current_row_ix += 1

    def __categorize_char(self, char: str):
        if char == '@':
            lexeme = self.__get_lexeme(
                TokenCategory.IDENTIFIER,
                IdentifierStates.INI_STATE,
                id_matrix.identifier_matrix,
            )
            self.__read_identifier(lexeme)
        elif char == '$':
            lexeme = self.__get_lexeme(
                TokenCategory.COMMENT,
                CommentStates.INI_STATE,
                comment_matrix.comment_matrix,
            )
            self.__read_comment(lexeme)
        elif char in 'NTBWFIER':  # Primeras letras de palabras reservadas
            lexeme = self.__get_lexeme(
                TokenCategory.KEYWORD,
                KeywordStates.INI_STATE,
                keyword_matrix.keyword_matrix,
            )
            self.__read_word(lexeme)
        elif char in dictionary.dictionary['delim_chars']:
            self.__read_delimitator()
        elif char in dictionary.dictionary['oper_chars']:
            self.__read_operator()
        elif char in dictionary.dictionary['spaces']:
            pass
        else:
            print(
                f"⚠️ Error: Unrecognized character '{char}' in line {self.current_row_ix + 1}, column {self.current_col_ix}")

    def __get_lexeme(self, token_category: TokenCategory, token_category_states, token_category_matrix) -> str:
        lexeme = ""
        state = token_category_states

        while self.current_col_ix < len(self.row_list[self.current_row_ix]):
            char = self.row_list[self.current_row_ix][self.current_col_ix]

            if state is not None:
                next_state = token_category_matrix.get(state, {}).get(char)
                if next_state is None and state != token_category_states.END_STATE:
                    print(
                        f"⚠️ Error: Malformed {token_category} '{lexeme}' in column[{self.current_col_ix}], row[{self.current_row_ix + 1}]")
                    return ""
                lexeme += char
                state = next_state
            else:
                print(
                    f"⚠️ Error: Malformed {token_category} '{lexeme}' in column[{self.current_col_ix}], row[{self.current_row_ix + 1}]")
                return ""

            self.current_col_ix += 1

            # Para comentarios, detener si se alcanza END_STATE
            if token_category == TokenCategory.COMMENT and state == CommentStates.END_STATE:
                break

        # Validar que se alcanzó un estado final válido
        if state != token_category_states.END_STATE:
            print(
                f"⚠️ Error: Incomplete {token_category} '{lexeme}' in column[{self.current_col_ix}], row[{self.current_row_ix + 1}]")
            return ""

        return lexeme

    def __read_identifier(self, lexeme):
        if len(lexeme[1:]) > 16: # Validation of lenght counting the '@' char
            print(f"⚠️ Error: IDENTIFIER '{lexeme}' lenght is {len(lexeme[1:])}. Lexeme must have 15 chars as maximum.")
            return

        if lexeme[1:] in self.keywords: # Validation of no keyword lexeme
            print(f"⚠️ Error: '{lexeme}' is a keyword.")
            return

        print(f"✅ Token IDENTIFIER valid: '{lexeme}' in line {self.current_row_ix + 1}")
        self.tokens.append(Token( #Si todo esta bien lo guardamos en el token
            TokenCategory.IDENTIFIER,
            lexeme,
            self.current_row_ix + 1,
            self.current_col_ix - len(lexeme)
        ))

    # TODO: Alfredo
    def __read_delimitator(self):
        
        pass

    def __read_comment(self, lexeme: str) -> None:
        if not lexeme:  # Si __get_lexeme devolvió un lexema vacío (error)
            return

        # Validar longitud máxima (100 caracteres)
        if len(lexeme) > 100:
            print(f"⚠️ Error: COMMENT '{lexeme}' length is {len(lexeme)}. Comments must be 100 chars or less.")
            return

        # Registrar el comentario como token
        print(f"✅ Token COMMENT valid: '{lexeme}' in line {self.current_row_ix + 1}")
        self.tokens.append(Token(
            TokenCategory.COMMENT,
            lexeme,
            self.current_row_ix + 1,
            self.current_col_ix - len(lexeme)
        ))

    def __read_word(self, lexeme: str) -> None:
        if not lexeme:  # Si __get_lexeme devolvió un lexema vacío (error)
            return

        # Validar que el lexema es una palabra reservada
        if lexeme not in self.keywords:
            print(
                f"⚠️ Error: Invalid KEYWORD '{lexeme}' in line {self.current_row_ix + 1}. Must be one of {self.keywords}.")
            return

        # Registrar la palabra reservada como token
        print(f"✅ Token KEYWORD valid: '{lexeme}' in line {self.current_row_ix + 1}")
        self.tokens.append(Token(
            TokenCategory.KEYWORD,
            lexeme,
            self.current_row_ix + 1,
            self.current_col_ix - len(lexeme)
        ))
    
    # TODO: Oski
    def __read_number(self):
        pass

    # TODO: Chaires
    def __read_operator(self):
        pass