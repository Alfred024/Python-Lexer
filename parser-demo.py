
from config import project_config
from classes.Lexer import Lexer
from classes.SymbolTable import SymbolTable
from classes.Parser import TableParser

symtab = SymbolTable()
lexer = Lexer(project_config['sample_code_file'], symtab)
parser = TableParser(symtab.tokens, symtab)
parser.parse()

# print("\nTokens:", symtab.tokens)
# print("\nSymbols declared:", symtab.all_symbols())
# print(parser.symtab.all_symbols())