import tkinter as tk
from tkinter import ttk, scrolledtext, font
from classes.Lexer import Lexer
from classes.Token import Token, TokenCategory
import re

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        
        # Configurar tags para colores de sintaxis (paleta más suave)
        self.tag_configure("comment", foreground="#65B741")    # Verde suave para comentarios
        self.tag_configure("keyword", foreground="#3559E0")    # Azul medio para palabras clave
        self.tag_configure("identifier", foreground="#FF6B6B") # Rojo coral para identificadores
        self.tag_configure("operator", foreground="#FF9843")   # Naranja suave para operadores
        self.tag_configure("number", foreground="#B15EFF")     # Violeta suave para números
        self.tag_configure("string", foreground="#4F709C")     # Azul grisáceo para strings
        self.tag_configure("error", background="#FFE4E4")      # Rojo muy claro para errores
        
        # Bind para detectar cambios en el texto
        self.bind('<KeyRelease>', self.on_key_release)
        
    def on_key_release(self, event=None):
        self.highlight_syntax()
        if hasattr(self, 'callback'):
            self.callback()
    
    def set_callback(self, callback):
        self.callback = callback
    
    def highlight_syntax(self):
        # Remover tags existentes
        for tag in ["comment", "keyword", "identifier", "operator", "number", "string", "error"]:
            self.tag_remove(tag, "1.0", "end")
            
        content = self.get("1.0", "end-1c")
        
        # Patrones para resaltado
        patterns = {
            "comment": r"\$.*$",
            "keyword": r"\b(Num|Text|Bool|If|Else|While|For|Write|Read|true|false)\b",
            "identifier": r"@\w+",
            "operator": r"[=+\-*/<>]",
            "number": r"\b\d+(\.\d+)?\b",
            "string": r'"[^"]*"'
        }
        
        for line_number, line in enumerate(content.split('\n'), 1):
            for pattern_name, pattern in patterns.items():
                for match in re.finditer(pattern, line):
                    start = f"{line_number}.{match.start()}"
                    end = f"{line_number}.{match.end()}"
                    self.tag_add(pattern_name, start, end)

class LexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Lexer IDE")
        
        # Configurar tema claro
        style = ttk.Style()
        style.configure(".", background="#F5F5F5", foreground="#333333")
        style.configure("Treeview", background="#FFFFFF", foreground="#333333", fieldbackground="#FFFFFF")
        style.configure("TLabel", background="#F5F5F5", foreground="#333333")
        style.configure("TLabelframe", background="#F5F5F5", foreground="#333333")
        style.configure("TButton", background="#E8E8E8", foreground="#333333")
        
        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.configure(bg="#F5F5F5")
        
        # Editor de código (lado izquierdo)
        self.code_frame = ttk.LabelFrame(root, text="Editor de Código")
        self.code_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Usar CustomText con fondo blanco
        self.code_editor = CustomText(self.code_frame, wrap=tk.WORD, bg="#FFFFFF", fg="#333333",
                                    insertbackground="#333333", font=('Consolas', 12))
        self.code_editor.pack(expand=True, fill="both", padx=5, pady=5)
        self.code_editor.set_callback(self.analyze_code_realtime)
        
        # Scrollbar para el editor
        code_scrollbar = ttk.Scrollbar(self.code_frame, orient="vertical", command=self.code_editor.yview)
        code_scrollbar.pack(side="right", fill="y")
        self.code_editor.configure(yscrollcommand=code_scrollbar.set)
        
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
        
        self.error_tree = ttk.Treeview(self.error_frame, columns=("Tipo", "Mensaje", "Línea", "Columna"))
        self.error_tree.heading("#0", text="")
        self.error_tree.heading("Tipo", text="Tipo")
        self.error_tree.heading("Mensaje", text="Mensaje")
        self.error_tree.heading("Línea", text="Línea")
        self.error_tree.heading("Columna", text="Columna")
        self.error_tree.column("#0", width=0, stretch=tk.NO)
        self.error_tree.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Configurar redimensionamiento
        root.grid_rowconfigure(0, weight=3)
        root.grid_rowconfigure(1, weight=1)
    
    def analyze_code_realtime(self):
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