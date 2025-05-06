# Classes
from classes.Token import Token, TokenCategory, TokenError
# Dictionary 📑
import data.alphabet as alphabet
# Transition matrixes 
    # Identifiers matrix
from data.TransitionMatrixes.identifier_matrix import IdentifierStates
import data.TransitionMatrixes.identifier_matrix as id_matrix
    # Delims matrix
from data.TransitionMatrixes.delimitator_matrix import DelimitatorStates
import data.TransitionMatrixes.delimitator_matrix as delim_matrix
    # Comments matrix
from data.TransitionMatrixes.comment_matrix import CommentStates
import data.TransitionMatrixes.comment_matrix as comment_matrix
    # Keywords matrix
from data.TransitionMatrixes.keyword_matrix import KeywordStates
import data.TransitionMatrixes.keyword_matrix as keyword_matrix
    # Operators matrix
from data.TransitionMatrixes.operator_matrix import OperatorStates
import data.TransitionMatrixes.operator_matrix as operator_matrix
    # Number matrix
from data.TransitionMatrixes.number_matrix import NumberStates
import data.TransitionMatrixes.number_matrix as number_matrix
    # Text matrix
from data.TransitionMatrixes.text_matrix import TextStates
import data.TransitionMatrixes.text_matrix as text_matrix


class Lexer:
    def __init__(self, file_input: str):
        self.tokens: list[Token] = []
        self.errors: list[TokenError] = []
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
        elif char in 'NTBWFIER': # Keywords first letters
            lexeme = self.__get_lexeme(
                TokenCategory.KEYWORD,
                KeywordStates.INI_STATE,
                keyword_matrix.keyword_matrix,
            )
            self.__read_keyword(lexeme)
        elif char in alphabet.alphabet['delim_chars']:
            lexeme = self.__get_lexeme(
                TokenCategory.DELIMITATOR,
                DelimitatorStates,
                delim_matrix.delimitator_matrix,
            )
            self.__read_delimitator(lexeme)
        elif char in alphabet.alphabet['oper_chars']:
            lexeme = self.__get_lexeme(
                TokenCategory.OPERATOR,
                OperatorStates,
                operator_matrix.operator_matrix,
            )
            self.__read_operator(lexeme)
        elif char in alphabet.alphabet['spaces']:
            self.__read_whitespace()
        elif char in alphabet.alphabet['numbers']:
            lexeme = self.__get_lexeme(
                TokenCategory.NUM,
                NumberStates,
                number_matrix.number_matrix,
            )
            self.__read_number(lexeme)
        elif char in alphabet.alphabet['text_delims']:
            lexeme = self.__get_lexeme(
                TokenCategory.TEXT,
                TextStates,
                text_matrix.text_matrix,
            )
            self.__read_text(lexeme)
        else:
            lexeme = self.__get_malformed_lexeme()
            self.errors.append(
                TokenError(
                    error_type=f'token_category Error',
                    message=f'The lexeme "{lexeme}" of category "token_category" is malformed',
                    line=self.current_row_ix + 1,
                    column=self.current_col_ix,
                )
            )

    def __get_lexeme(self, token_category: TokenCategory, token_category_states, token_category_matrix) -> str:
        lexeme = ""
        state = token_category_states.INI_STATE
        pos = self.current_col_ix

        while pos < len(self.row_list[self.current_row_ix]):
            char = self.row_list[self.current_row_ix][pos]
            state  = token_category_matrix.get(state, {}).get(char)

            if state is None:
                break

            lexeme += char
            pos += 1

            if state == token_category_states.END_STATE:
                break

            if token_category == TokenCategory.COMMENT and state == CommentStates.END_STATE:
                break

        self.current_col_ix = pos - 1
        return lexeme

    def __get_malformed_lexeme(self):
        lexeme = ""
        pos = self.current_col_ix

        while pos < len(self.row_list[self.current_row_ix]):
            char = self.row_list[self.current_row_ix][pos]
            lexeme += char
            pos += 1
            
            if (char in alphabet.alphabet['spaces'] ):
                self.current_col_ix = pos - 1
                return lexeme
            
        self.current_col_ix = pos - 1
        return lexeme

    def __read_identifier(self, lexeme):
        if len(lexeme[1:]) > 16:
            self.errors.append(
                TokenError(
                    error_type=f'{TokenCategory.IDENTIFIER} Error',
                    message=f" '{lexeme}' exceed 15 chars limit.",
                    line=self.current_row_ix + 1,
                    column=self.current_col_ix,
                )
            )
            return
        
        if len(lexeme[1:]) == 1:
            self.errors.append(
                TokenError(
                    error_type=f'{TokenCategory.IDENTIFIER} Error',
                    message=f" '{lexeme}' must contain least one char.",
                    line=self.current_row_ix + 1,
                    column=self.current_col_ix,
                )
            )
            return

        if lexeme[1:] in self.keywords:
            self.errors.append(
                TokenError(
                    error_type=f'{TokenCategory.IDENTIFIER} Error',
                    message=f"'{lexeme}' isn´t a keyword.",
                    line=self.current_row_ix + 1,
                    column=self.current_col_ix,
                )
            )
            return

        self.tokens.append(
            Token(
                TokenCategory.IDENTIFIER,
                lexeme,
                self.current_row_ix + 1,
                self.current_col_ix
            )
        )

    def __read_delimitator(self, lexeme):
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
                self.current_row_ix + 1,
                self.current_col_ix,
            )
        )

    def __read_operator(self, lexeme):
        token_category : TokenCategory
                
        if(lexeme in ['+', '-', '*', '/']):
            token_category = TokenCategory.ARIT_OPER
        elif(lexeme in ['==', '!=', '<', '>', '<=', '>=']):
            token_category = TokenCategory.REL_OPER
        elif(lexeme in ['&&', '||', '!']):
            token_category = TokenCategory.LOG_OPER
        elif(lexeme == '='):
            token_category = TokenCategory.ASIG_OPER
        elif(lexeme == '++'):
            token_category = TokenCategory.INC_OPER
        elif(lexeme == '--'):
            token_category = TokenCategory.DEC_OPER
        
        self.tokens.append(
            Token(
                token_category,
                lexeme,
                self.current_row_ix + 1,
                self.current_col_ix,
            )
        )
    
    def __read_comment(self, lexeme: str):
        self.tokens.append(Token(
            TokenCategory.COMMENT,
            lexeme,
            self.current_row_ix + 1,
            self.current_col_ix
        ))

    def __read_keyword(self, lexeme: str) -> None:
        if not lexeme:
            return

        if lexeme not in self.keywords:
            self.errors.append(
                TokenError(
                    error_type='Keyword Error',
                    message=f"'{lexeme}' isn´t a keyword.",
                    line=self.current_row_ix + 1,
                    column=self.current_col_ix,
                )
            )
            return

        if lexeme in ['True', 'False']:
            self.tokens.append(Token(
                TokenCategory.BOOL,
                lexeme,
                self.current_row_ix + 1,
                self.current_col_ix
            ))
            return

        self.tokens.append(Token(
            TokenCategory.KEYWORD,
            lexeme,
            self.current_row_ix + 1,
            self.current_col_ix
        ))
    
    def __read_number(self, lexeme: str) -> None:
        self.tokens.append(Token(
            TokenCategory.NUM,
            lexeme,
            self.current_row_ix + 1,
            self.current_col_ix
        ))

    def __read_text(self, lexeme: str) -> None:
        self.tokens.append(Token(
            TokenCategory.TEXT,
            lexeme,
            self.current_row_ix + 1,
            self.current_col_ix
        ))
    
    def __read_whitespace(self):
        pos = self.current_col_ix
        char = self.row_list[self.current_row_ix][pos]

        while char in alphabet.alphabet['spaces'] and pos < len(self.row_list[self.current_row_ix]):
            char = self.row_list[self.current_row_ix][pos]
            pos += 1
