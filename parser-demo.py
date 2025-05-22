
from config import project_config
from classes.Lexer import Lexer
from classes.SymbolTable import SymbolTable
from classes.Parser import TableParser

symtab = SymbolTable()
lexer = Lexer(project_config['sample_code_file'], symtab)
print(f'Tokens \n')
for token in lexer.symtab.tokens:
    print(token)
print('\n')

parser = TableParser(symtab.tokens, symtab)

try:
    parser.parse()
    print("Sintactic succesfull!!")
except SyntaxError as e:
    print("Sintactic error:", e)

# print("\nTokens:", symtab.tokens)
# print("\nSymbols declared:", symtab.all_symbols())