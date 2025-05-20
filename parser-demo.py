from classes.Lexer import Lexer
from classes.SymbolTable import SymbolTable
from classes.Parser import TableParser

symtab = SymbolTable()
lexer = Lexer("temp_code.txt", symtab)
parser = TableParser(symtab.tokens, symtab)

try:
    parser.parse()
    print("Sintactic succesfull!!")
except SyntaxError as e:
    print("Sintactic error:", e)

print("\nTokens:", symtab.tokens)
print("\nSymbols declared:", symtab.all_symbols())