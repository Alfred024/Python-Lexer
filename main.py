import config
from classes.Lexer import Lexer
<<<<<<< HEAD
from classes.Token import TokenCategory
from config import project_config
import tkinter as tk
from gui import LexerGUI

if __name__ == "__main__":
    # Iniciar la interfaz gráfica
    root = tk.Tk()
    app = LexerGUI(root)
    root.geometry("1200x800")
    root.mainloop()
    
    # # Token creation    
    # lexer = Lexer(project_config['sample_code_file'])
    # for token in lexer.tokens:
    #     print(token)
        
    
=======

if __name__ == "__main__":
    lexer = Lexer(config.DELIMS_FILE)

    print('Tokens List: \n')
    for token in lexer.tokens:
        print(token)
>>>>>>> 74db4672bad86f8c5fb1590428ace9c756181ab9
