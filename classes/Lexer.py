# Classes
from classes.Token import Token, TokenCategory
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

class Lexer:
    def __init__(self, file_input: str):
        self.tokens: list[Token] = []
        self.errors: list[dict] = []  # Lista para almacenar errores
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
            pass
        else:
            # TODO: Mientras le sigan entrando caracteres fuera de los casos contempados, sigue acumulando el lexema para ir  formando el Token inválido
            self.errors.append({
                'tipo': 'Char don´t recognize in alpahber',
                'mensaje': f"Caracter '{char}' no reconocido",
                'linea': self.current_row_ix + 1,
                'columna': self.current_col_ix
            })

    def __get_lexeme(self, token_category: TokenCategory, token_category_states, token_category_matrix) -> str:
        lexeme = ""
        state = token_category_states.INI_STATE
        pos = self.current_col_ix

        while pos < len(self.row_list[self.current_row_ix]):
            char = self.row_list[self.current_row_ix][pos]
            print(f'Voy a buscar el char {char} en el state {state}')
            state  = token_category_matrix.get(state, {}).get(char)

            if state is None:
                self.errors.append({
                'tipo': f'Error en {token_category}',
                'mensaje': f"Token malformado '{lexeme}'",
                'linea': self.current_row_ix + 1,
                'columna': self.current_col_ix
                })
                break

            state  = state
            lexeme += char
            pos += 1

            if state == token_category_states.END_STATE:
                break

            if token_category == TokenCategory.COMMENT and state == CommentStates.END_STATE:
                break

        self.current_col_ix = pos - 1
        return lexeme

    def __read_identifier(self, lexeme):
        if len(lexeme[1:]) > 16:
            self.errors.append({
                'tipo': 'Error de Identificador',
                'mensaje': f"Identificador '{lexeme}' excede el límite de 15 caracteres",
                'linea': self.current_row_ix + 1,
                'columna': self.current_col_ix
            })
            return

        if lexeme[1:] in self.keywords:
            self.errors.append({
                'tipo': 'Error de Identificador',
                'mensaje': f"'{lexeme}' es una palabra reservada",
                'linea': self.current_row_ix + 1,
                'columna': self.current_col_ix
            })
            return

        print(f"✅ Token IDENTIFIER valid: '{lexeme}' in line {self.current_row_ix + 1}")
        self.tokens.append(Token( #Si todo esta bien lo guardamos en el token
            TokenCategory.IDENTIFIER,
            lexeme,
            self.current_row_ix + 1,
            self.current_col_ix
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
                self.current_row_ix + 1,
                self.current_col_ix,
            )
        )

    def __read_operator(self, lexeme):
        print(f"✅ Token OPERATOR valid: '{lexeme}' in line {self.current_row_ix + 1}")
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
        if len(lexeme) > 100:
            self.errors.append({
                'tipo': 'Error de Comentario',
                'mensaje': f"El comentario excede el límite de 100 caracteres",
                'linea': self.current_row_ix + 1,
                'columna': self.current_col_ix
            })
            return

        print(f"✅ Token COMMENT valid: '{lexeme}' in line {self.current_row_ix + 1}")
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
            self.errors.append({
                'tipo': 'Error de Palabra Reservada',
                'mensaje': f"'{lexeme}' no es una palabra reservada válida",
                'linea': self.current_row_ix + 1,
                'columna': self.current_col_ix
            })
            return

        # TODO: Esta validación está duplicada
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
            self.current_col_ix
        ))
    
    # TODO: Oski
    def __read_number(self):
        pass
    
    def __read_whitespace(self):
        pos = self.current_col_ix
        char = self.row_list[self.current_row_ix][pos]
        
        while char in alphabet.alphabet['spaces'] and pos < len(self.row_list[self.current_row_ix]):
            print('Reading white space...')
            char = self.row_list[self.current_row_ix][pos]
            pos += 1