from classes.Lexer import Lexer
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
        
    