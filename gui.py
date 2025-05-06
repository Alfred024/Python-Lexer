import tkinter as tk
from tkinter import ttk, scrolledtext
import re
from classes.SymbolTable import SymbolTable
from classes.Lexer import Lexer
from classes.Token import TokenCategory, Token, TokenError


# ───────────────────────────── Editor con resaltado ──────────────────────────
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Paleta de colores
        self.tag_configure("comment",    foreground="#65B741")
        self.tag_configure("keyword",    foreground="#3559E0")
        self.tag_configure("identifier", foreground="#FF6B6B")
        self.tag_configure("operator",   foreground="#00FF00")
        self.tag_configure("number",     foreground="#B15EFF")
        self.tag_configure("string",     foreground="#4F709C")
        self.tag_configure("error",      background="#FFE4E4")

        self.bind("<KeyRelease>", self.on_key_release)

    def set_callback(self, cb):
        self._callback = cb

    def on_key_release(self, event=None):
        self.highlight_syntax()
        if hasattr(self, "_callback"):
            self._callback()

    def highlight_syntax(self):
        for tag in ["comment", "keyword", "identifier", "operator",
                    "number", "string", "error"]:
            self.tag_remove(tag, "1.0", "end")

        content = self.get("1.0", "end-1c")
        patterns = {
            "comment":    r"\$.*$",
            "keyword":    r"\b(Num|Text|Bool|If|Else|While|For|Write|Read|True|False)\b",
            "identifier": r"@\w+",
            "operator":   r"[=+\-*/<>.]",
            "number":     r"\b\d+(\.\d+)?\b",
            "string":     r'"[^"]*"'
        }

        for ln, line in enumerate(content.split("\n"), 1):
            for tag, pat in patterns.items():
                for m in re.finditer(pat, line):
                    start, end = f"{ln}.{m.start()}", f"{ln}.{m.end()}"
                    self.tag_add(tag, start, end)


# ───────────────────────────── GUI principal ─────────────────────────────────
class LexerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Lexer IDE")

        # Tema claro
        style = ttk.Style()
        style.configure(".", background="#F5F5F5", foreground="#333333")
        style.configure("Treeview", fieldbackground="#FFFFFF",
                        background="#FFFFFF", foreground="#333333")

        # Grid del root
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=3)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.configure(bg="#F5F5F5")

        # ── Editor ──────────────────────────────────────────────────────────
        self.code_frame = ttk.LabelFrame(root, text="Code Editor")
        self.code_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.code_editor = CustomText(self.code_frame, wrap=tk.WORD,
                                      bg="#FFFFFF", fg="#333333",
                                      insertbackground="#333333",
                                      font=("Consolas", 12))
        self.code_editor.pack(expand=True, fill="both", padx=5, pady=5)
        self.code_editor.set_callback(self.analyze_code_realtime)

        code_scroll = ttk.Scrollbar(self.code_frame, orient="vertical",
                                    command=self.code_editor.yview)
        code_scroll.pack(side="right", fill="y")
        self.code_editor.configure(yscrollcommand=code_scroll.set)

        # ── Vista de tokens ────────────────────────────────────────────────
        self.token_frame = ttk.LabelFrame(root, text="Tokens")
        self.token_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.token_tree = ttk.Treeview(
            self.token_frame,
            columns=("Type", "Value", "Line", "Column"),
            show="headings"
        )
        for col in ("Type", "Value", "Line", "Column"):
            self.token_tree.heading(col, text=col)
        self.token_tree.pack(expand=True, fill="both", padx=5, pady=5)

        # ── Vista tabla de símbolos ────────────────────────────────────────
        self.sym_frame = ttk.LabelFrame(root, text="Symbol Table")
        self.sym_frame.grid(row=1, column=0, padx=5, pady=5,
                            columnspan=1, sticky="nsew")
        self.sym_tree = ttk.Treeview(
            self.sym_frame,
            columns=("Name", "VarType", "Line"),
            show="headings"
        )
        for col in ("Name", "VarType", "Line"):
            self.sym_tree.heading(col, text=col)
        self.sym_tree.pack(expand=True, fill="both", padx=5, pady=5)

        # ── Vista de errores ───────────────────────────────────────────────
        self.error_frame = ttk.LabelFrame(root, text="Errors")
        self.error_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.error_tree = ttk.Treeview(
            self.error_frame,
            columns=("Type", "Message", "Line", "Column"),
            show="headings"
        )
        for col in ("Type", "Message", "Line", "Column"):
            self.error_tree.heading(col, text=col)
        self.error_tree.pack(expand=True, fill="both", padx=5, pady=5)

    # ───────────────────────── Actualizar GUI ─────────────────────────────
    def analyze_code_realtime(self):
        # Limpiar vistas
        for tree in (self.token_tree, self.sym_tree, self.error_tree):
            tree.delete(*tree.get_children())

        # Obtener código y guardarlo temporalmente
        code = self.code_editor.get(1.0, tk.END)
        with open("temp_code.txt", "w", encoding="utf-8") as f:
            f.write(code)

        # Crear tabla de símbolos y lexer
        symtab = SymbolTable()
        lexer = Lexer("temp_code.txt", symtab)

        # ── Tokens
        for tok in symtab.tokens:
            self.token_tree.insert("", tk.END, values=(
                tok.category.value,
                tok.value,
                tok.row,
                tok.col
            ))

        # ── Símbolos (identificadores declarados)
        for name, info in symtab.all_symbols().items():
            self.sym_tree.insert("", tk.END,
                                 values=(name, info.var_type, info.declared_line))

        # ── Errores
        for err in lexer.errors:
            self.error_tree.insert("", tk.END, values=(
                err._type, err._message, err._line, err._column
            ))


# # ────────────────────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.geometry("1200x800")
#     app = LexerGUI(root)
#     root.mainloop()
