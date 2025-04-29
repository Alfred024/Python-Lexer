from classes.Lexer import Lexer
from config import project_config

if __name__ == "__main__":
    lexer = Lexer(project_config['delims_file'])
    for token in lexer.tokens:
        print(token)