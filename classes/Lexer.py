# Classes
from classes.Token import Token, TokenCategory
# Dictionary 📑
import data.dictionary as dictionary
# Transition matrixes 
    # Identifiers matrix
from data.TransitionMatrixes.identifier_matrix import IdentifierStates
import data.TransitionMatrixes.identifier_matrix as id_matrix
    # Delims matrix


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
                IdentifierStates,
                id_matrix.identifier_matrix,
            )
            self.__read_identifier(lexeme)
        elif char in dictionary.dictionary['delim_chars']:
            lexeme = self.__get_lexeme(
                TokenCategory.DELIMITATOR,
                DelimitatorStates,
                delim_matrix.delimitator_matrix,
            )
            self.__read_delimitator(lexeme)
        elif char in dictionary.dictionary['spaces']:
            pass
        elif char == '$':
            pass
        else:
            pass

    def __get_lexeme(self, token_category : TokenCategory, token_category_states, token_category_matrix) -> str:
        lexeme = ""
        state = token_category_states.INI_STATE 
        
        while self.current_col_ix < len(self.row_list[self.current_row_ix]): 
            char = self.row_list[self.current_row_ix][self.current_col_ix]
            print(F'Char: {char}')
            # Check if the state exists in the transition matrix
            if(state != None):
                state = token_category_matrix.get(state, {}).get(char) # Get new state lexeme
                lexeme += char
                if(state == token_category_states.END_STATE):
                    break
            else:
                print(f"⚠️ Error: Malformed {token_category} '{lexeme}' in column[{self.current_col_ix}], row[{self.current_row_ix + 1}]")
                return ""
            self.current_col_ix += 1
        
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

    def __read_delimitator(self, lexeme):
        print(f"✅ Token DELIMITATOR valid: '{lexeme}' in line {self.current_row_ix + 1}")
        token_category : TokenCategory
                
        if(lexeme == '('):
            token_category = TokenCategory.DELIM_PARENT_LEFT
        elif(lexeme == ')'):
            token_category = TokenCategory.DELIM_PARENT_RIGHT
        elif(lexeme == '{'):
            token_category = TokenCategory.DELIM_BRACE_LEFT
        elif(lexeme == '}'):
            token_category = TokenCategory.DELIM_BRACE_RIGHT
        else:
            token_category = TokenCategory.DELIM_POINT
        
        self.tokens.append(
            Token(
                token_category,
                lexeme,
                self.current_row_ix,
                self.current_col_ix,
            )
        )

    def __read_comment(self, lexeme: str) -> None:
        # Validar que el lexema comienza con '$'
        if not lexeme.startswith('$'):
            print(
                f"⚠️ Error: Invalid COMMENT '{lexeme}' in line {self.current_row_ix + 1}. Comments must start with '$'.")
            return

        # Opcional: Validar longitud máxima (100 caracteres)
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