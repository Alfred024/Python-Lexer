import config
from classes.Lexer import Lexer

if __name__ == "__main__":
    lexer = Lexer(config.DELIMS_FILE)

    print('Tokens List: \n')
    for token in lexer.tokens:
        print(token)