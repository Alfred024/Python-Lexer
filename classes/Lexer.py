# -*- coding: utf-8 -*-
# Classes
from classes.Token import Token, TokenCategory, TokenCode, TokenError
from classes.SymbolTable import SymbolTable
from classes.ErrorsStack import ErrorsStack 
# Dictionary 📑
import data.alphabet as alphabet
# Transition matrixes
from data.TransitionMatrixes.identifier_matrix import IdentifierStates
import data.TransitionMatrixes.identifier_matrix as id_matrix
from data.TransitionMatrixes.delimitator_matrix import DelimitatorStates
import data.TransitionMatrixes.delimitator_matrix as delim_matrix
from data.TransitionMatrixes.comment_matrix import CommentStates
import data.TransitionMatrixes.comment_matrix as comment_matrix
from data.TransitionMatrixes.keyword_matrix import KeywordStates
import data.TransitionMatrixes.keyword_matrix as keyword_matrix
from data.TransitionMatrixes.operator_matrix import OperatorStates
import data.TransitionMatrixes.operator_matrix as operator_matrix
from data.TransitionMatrixes.number_matrix import NumberStates
import data.TransitionMatrixes.number_matrix as number_matrix
from data.TransitionMatrixes.text_matrix import TextStates
import data.TransitionMatrixes.text_matrix as text_matrix


class Lexer:

    def __init__(self, file_input: str, symtab: SymbolTable):
        self.symtab = symtab
        self.errors = ErrorsStack()
        self.file_input = file_input
        self.current_row_ix = 0
        self.current_col_ix = 0
        self.row_list = []
        
        self.declaration_types = {"Num", "Text", "Bool"}
        
        self.keywords = [
            "While", "For", "If", "Else", "Read", "Write",
            "Num", "Text", "Bool", "True", "False"
        ]
        self.__read_input()

    def __read_input(self):
        with open(self.file_input, 'r') as file:
            self.row_list = [line.rstrip("\n") for line in file]

        while self.current_row_ix < len(self.row_list):
            self.current_col_ix = 0
            while self.current_col_ix < len(self.row_list[self.current_row_ix]):
                ch = self.row_list[self.current_row_ix][self.current_col_ix]
                self.__categorize_char(ch)
                self.current_col_ix += 1
            self.current_row_ix += 1

    def __categorize_char(self, char: str):
        if char == '@':
            lexeme = self.__get_lexeme(TokenCategory.IDENTIFIER,
                                        IdentifierStates,
                                        id_matrix.identifier_matrix)
            self.__read_identifier(lexeme)

        elif char == '$':
            lexeme = self.__get_lexeme(TokenCategory.COMMENT,
                                        CommentStates,
                                        comment_matrix.comment_matrix)
            self.__read_comment(lexeme)

        elif char in 'NTBWFIER':  # inicio posible keyword
            lexeme = self.__get_lexeme(TokenCategory.KEYWORD,
                                        KeywordStates,
                                        keyword_matrix.keyword_matrix)
            self.__read_keyword(lexeme)

        elif char in alphabet.alphabet['delim_chars']:
            lexeme = self.__get_lexeme(TokenCategory.DELIMITATOR,
                                        DelimitatorStates,
                                        delim_matrix.delimitator_matrix)
            self.__read_delimitator(lexeme)

        elif char in alphabet.alphabet['oper_chars']:
            lexeme = self.__get_lexeme(TokenCategory.OPERATOR,
                                        OperatorStates,
                                        operator_matrix.operator_matrix)
            self.__read_operator(lexeme)
        elif char in alphabet.alphabet['spaces']:
            self.__read_whitespace()
        elif char in alphabet.alphabet['numbers']:
            lexeme = self.__get_lexeme(TokenCategory.NUM,
                                        NumberStates,
                                        number_matrix.number_matrix)
            self.__read_number(lexeme)

        elif char in alphabet.alphabet['text_delims']:
            lexeme = self.__get_lexeme(TokenCategory.TEXT,
                                        TextStates,
                                        text_matrix.text_matrix)
            self.__read_text(lexeme)
        else:
            self.__set_error(TokenCategory.ERROR, char)

    def __get_lexeme(self, token_category, states, matrix) -> str:
        lexeme = ""
        state = states.INI_STATE

        while self.current_col_ix < len(self.row_list[self.current_row_ix]):
            ch = self.row_list[self.current_row_ix][self.current_col_ix]
            state = matrix.get(state, {}).get(ch)

            if state is None:
                break
            
            if state == states.ERROR_STATE:
                self.__set_error(token_category, lexeme)
                return ''

            lexeme += ch
            self.current_col_ix += 1

            if state == states.END_STATE:
                break
        
        self.current_col_ix -= 1
        return lexeme

    def __get_malformed_lexeme(self, lexeme = ''):
        pos = self.current_col_ix
        while pos < len(self.row_list[self.current_row_ix]):
            ch = self.row_list[self.current_row_ix][pos]
            lexeme += ch
            pos += 1
            if ch in alphabet.alphabet['spaces']:
                break
        self.current_col_ix = pos - 1
        self.errors.push(TokenError(
            error_type='Lexical Error',
            message=f'Lexeme "{lexeme}" not recognized.',
            line=self.current_row_ix + 1,
            column=self.current_col_ix
        ))
        return lexeme

    def __set_error(self, token_category : TokenCategory, lexeme):
        if token_category == TokenCategory.IDENTIFIER:
            lexeme = self.__get_malformed_lexeme(lexeme=lexeme)
            self.errors.push(TokenError(
                error_type='Identifier',
                message=f"'{lexeme}' formed incorrectly.",
                line=self.current_row_ix + 1,
                column=self.current_col_ix
            ))
            return lexeme
        if token_category == TokenCategory.ERROR:
            lexeme = self.__get_malformed_lexeme(lexeme=lexeme)
            self.errors.push(TokenError(
                error_type='Bad entry',
                message=f"'{lexeme}' can´t be assign a token category.",
                line=self.current_row_ix + 1,
                column=self.current_col_ix
            ))
        else:
            print('NO IDENTIFICADO...')
            pass

    def __read_identifier(self, lexeme):
        if lexeme == '':
            return
        
        if len(lexeme) <= 1 or len(lexeme) > 16:
            self.errors.push(TokenError(
                error_type='Identifier',
                message=f"'{lexeme}' is too large.",
                line=self.current_row_ix + 1,
                column=self.current_col_ix
            ))
            return
        
        if lexeme[1:] in self.keywords:
            self.errors.push(TokenError(
                error_type='Identifier',
                message=f"'{lexeme}' can´t be a keyword.",
                line=self.current_row_ix + 1,
                column=self.current_col_ix
            ))
            return

        tok = Token(
                    TokenCategory.IDENTIFIER,
                    TokenCode.IDENTIFIER,
                    lexeme,
                    self.current_row_ix + 1,
                    self.current_col_ix)

        prev_tok = self.symtab.tokens[-1] if self.symtab.tokens else None
        declares = prev_tok and prev_tok.category == TokenCategory.KEYWORD \
                   and prev_tok.value in self.declaration_types

        if declares:
            try:
                self.symtab.declare(lexeme, prev_tok.value, tok.row)
            except ValueError as e:
                self.errors.push(TokenError(
                    error_type="Duplicate Identifier",
                    message=str(e),
                    line=tok.row,
                    column=tok.column
                ))
        else:
            if not self.symtab.is_declared(lexeme):
                self.errors.push(TokenError(
                    error_type="Undeclared Identifier",
                    message=f"Var '{lexeme}' used with no declaration.",
                    line=tok.row,
                    column=tok.column
                ))

        self.symtab.add_token(tok)

    def __read_delimitator(self, lexeme):
        token_categories = {
            '(': TokenCategory.DELIM_PARENT_LEFT,
            ')': TokenCategory.DELIM_PARENT_RIGHT,
            '{': TokenCategory.DELIM_BRACE_LEFT,
            '}': TokenCategory.DELIM_BRACE_RIGHT,
            '.': TokenCategory.DELIM_POINT
        }
        
        token_codes = {
            '(': TokenCode.DELIM_PARENT_LEFT,
            ')': TokenCode.DELIM_PARENT_RIGHT,
            '{': TokenCode.DELIM_BRACE_LEFT,
            '}': TokenCode.DELIM_BRACE_RIGHT,
            '.': TokenCode.DELIM_POINT
        }
        
        tok = Token(
                    token_categories[lexeme], 
                    token_codes[lexeme],
                    lexeme,
                    self.current_row_ix + 1,
                    self.current_col_ix)
        self.symtab.add_token(tok)

    def __read_operator(self, lexeme):
        if lexeme in ['+', '-', '*', '/']:
            tk = TokenCategory.ARIT_OPER
        elif lexeme in ['==', '!=', '<', '>', '<=', '>=']:
            tk = TokenCategory.REL_OPER
        elif lexeme in ['&&', '||', '!']:
            tk = TokenCategory.LOG_OPER
        elif lexeme == '=':
            tk = TokenCategory.ASIG_OPER
        elif lexeme == '++':
            tk = TokenCategory.INC_OPER
        else:
            tk = TokenCategory.DEC_OPER

        self.symtab.add_token(Token(
                                    tk, 
                                    TokenCode.OPERATOR,
                                    lexeme,
                                    self.current_row_ix + 1,
                                    self.current_col_ix))

    def __read_comment(self, lexeme):
        self.symtab.add_token(Token(
                                    TokenCategory.COMMENT, 
                                    TokenCode.COMMENT,
                                    lexeme,
                                    self.current_row_ix + 1,
                                    self.current_col_ix))

    def __read_keyword(self, lexeme):
        if not lexeme or lexeme not in self.keywords:
            self.errors.push(TokenError(
                error_type='Keyword Error',
                message=f"'{lexeme}' no es keyword.",
                line=self.current_row_ix + 1,
                column=self.current_col_ix
            ))
            return

        tk_type = TokenCategory.BOOL if lexeme in ['True', 'False'] \
                  else TokenCategory.KEYWORD
        tk_code = TokenCode.BOOL if lexeme in ['True', 'False'] \
                  else TokenCode.KEYWORD      
            
        self.symtab.add_token(Token(tk_type, 
                                    tk_code,    
                                    lexeme,
                                    self.current_row_ix + 1,
                                    self.current_col_ix))

    def __read_number(self, lexeme):
        self.symtab.add_token(Token(TokenCategory.NUM, 
                                    TokenCode.NUM,
                                    lexeme,
                                    self.current_row_ix + 1,
                                    self.current_col_ix))

    def __read_text(self, lexeme):
        self.symtab.add_token(Token(TokenCategory.TEXT, 
                                    TokenCode.TEXT,
                                    lexeme,
                                    self.current_row_ix + 1,
                                    self.current_col_ix))

    def __read_whitespace(self):
        pos = self.current_col_ix
        while pos < len(self.row_list[self.current_row_ix]) and \
              self.row_list[self.current_row_ix][pos] in alphabet.alphabet['spaces']:
            pos += 1
        self.current_col_ix = pos - 1
