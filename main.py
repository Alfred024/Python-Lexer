from classes.Lexer import Lexer
from config import project_config

if __name__ == "__main__":
    lexer = Lexer(project_config['sample_code_file'])
    # Imprimir tokens para probar
    for token in lexer.tokens:
        print(token)