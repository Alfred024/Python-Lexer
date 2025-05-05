import tkinter as tk
from tkinter import ttk, scrolledtext
from classes.Lexer import Lexer
from classes.Token import Token, TokenCategory

class LexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Lexer IDE")
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        
        # Editor de código (lado izquierdo)
        self.code_frame = ttk.LabelFrame(root, text="Editor de Código")
        self.code_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.code_editor = scrolledtext.ScrolledText(self.code_frame, wrap=tk.WORD)
        self.code_editor.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Pila de tokens (lado derecho)
        self.token_frame = ttk.LabelFrame(root, text="Pila de Tokens")
        self.token_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.token_tree = ttk.Treeview(self.token_frame, columns=("Tipo", "Valor", "Línea", "Columna"))
        self.token_tree.heading("#0", text="")
        self.token_tree.heading("Tipo", text="Tipo")
        self.token_tree.heading("Valor", text="Valor")
        self.token_tree.heading("Línea", text="Línea")
        self.token_tree.heading("Columna", text="Columna")
        self.token_tree.column("#0", width=0, stretch=tk.NO)
        self.token_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Panel de errores (abajo)
        self.error_frame = ttk.LabelFrame(root, text="Pila de Errores")
        self.error_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Cambiar el ScrolledText por un Treeview para los errores
        self.error_tree = ttk.Treeview(self.error_frame, columns=("Tipo", "Mensaje", "Línea", "Columna"))
        self.error_tree.heading("#0", text="")
        self.error_tree.heading("Tipo", text="Tipo")
        self.error_tree.heading("Mensaje", text="Mensaje")
        self.error_tree.heading("Línea", text="Línea")
        self.error_tree.heading("Columna", text="Columna")
        self.error_tree.column("#0", width=0, stretch=tk.NO)
        self.error_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.error_text = scrolledtext.ScrolledText(self.error_frame, height=5, wrap=tk.WORD)
        self.error_text.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Botón de análisis
        self.analyze_button = ttk.Button(root, text="Analizar Código", command=self.analyze_code)
        self.analyze_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Configurar redimensionamiento
        root.grid_rowconfigure(0, weight=3)
        root.grid_rowconfigure(1, weight=1)
    
    def analyze_code(self):
        # Limpiar visualizaciones anteriores
        self.token_tree.delete(*self.token_tree.get_children())
        self.error_tree.delete(*self.error_tree.get_children())
        
        # Obtener el código del editor
        code = self.code_editor.get(1.0, tk.END)
        
        # Guardar el código en un archivo temporal
        with open("temp_code.txt", "w") as f:
            f.write(code)
        
        # Crear instancia del lexer y analizar
        lexer = Lexer("temp_code.txt")
        
        # Mostrar tokens en el árbol
        for token in lexer.tokens:
            self.token_tree.insert("", tk.END, values=(
                token.category.value,
                token.value,
                token.row,
                token.col
            ))
            
        # Mostrar errores en el árbol de errores
        for error in lexer.errors:
            self.error_tree.insert("", tk.END, values=(
                error['tipo'],
                error['mensaje'],
                error['linea'],
                error['columna']
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = LexerGUI(root)
    root.geometry("1200x800")
    root.mainloop()