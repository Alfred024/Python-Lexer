from classes.Lexer import Lexer
from classes.Token import TokenCategory
from config import project_config

if __name__ == "__main__":
        
    lexer = Lexer(project_config['opers_file'])
    for token in lexer.tokens:
        print(token)