# Classes
from classes.Token import Token, TokenCategory
# Dictionary 📑
import data.dictionary as dictionary
# Transition matrixes 
    # Identifiers matrix
from data.TransitionMatrixes.identifier_matrix import IdentifierStates
import data.TransitionMatrixes.identifier_matrix as id_matrix
    # Delims matrix
from data.TransitionMatrixes.delimitator_matrix import DelimitatorStates
import data.TransitionMatrixes.delimitator_matrix as delim_matrix

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
            self.__read_delimitator()
        elif char in dictionary.dictionary['oper_chars']:
            pass
        elif char in dictionary.dictionary['spaces']:
            pass
        elif char == '$':
            pass
        else:
            pass

    def __get_lexeme(self, token_category : TokenCategory, token_category_states, token_category_matrix) -> str:
        lexeme = ""
        state = token_category_states.INI_STATE 
        
        while self.current_col_ix + 1 < len(self.row_list[self.current_row_ix]): 
            char = self.row_list[self.current_row_ix][self.current_col_ix]

            # Check if the state exists in the transition matrix
            if(state != None):
                state = token_category_matrix.get(state, {}).get(char) # Get new state lexeme
                lexeme += char
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

    def __read_delimitator(self):
        
        pass

    def __read_comment(self):
        pass

    def __read_word(self):
        pass

    def __read_number(self):
        pass

    def __read_operator(self):
        pass

    def __is_whitespace(self) -> bool:
        pass

    def __error_char_index(self) -> int:
        pass