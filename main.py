import config
from classes.Lexer import Lexer
from classes.SymbolTable import SymbolTable
from config import project_config
import tkinter as tk
from gui import LexerGUI

if __name__ == "__main__":
    # Iniciar la interfaz gráfica
    root = tk.Tk()
    app = LexerGUI(root)
    root.geometry("1200x800")
    root.mainloop()        