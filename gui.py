import tkinter as tk
from tkinter import ttk, scrolledtext, PhotoImage, Toplevel, Label
import re
from classes.SymbolTable import SymbolTable
from classes.Lexer import Lexer
from classes.Token import TokenCategory, Token, TokenError
import subprocess
import os
import sys


# ───────────────────────────── Editor con resaltado ──────────────────────────
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Paleta de colores
        self.tag_configure("comment", foreground="#65B741")
        self.tag_configure("keyword", foreground="#3559E0")
        self.tag_configure("identifier", foreground="#FF6B6B")
        self.tag_configure("operator", foreground="#00FF00")
        self.tag_configure("number", foreground="#B15EFF")
        self.tag_configure("string", foreground="#4F709C")
        self.tag_configure("error_line", background="#FFE4E4")  # Fondo rojo claro para líneas con error
        self.tag_configure("error_char", background="#FF9999")  # Rojo más intenso para el carácter específico

        # Configuración de números de línea
        self._line_numbers = tk.Text(
            self.master, width=4,
            padx=4, pady=5,
            takefocus=0,
            border=0,
            background='#F0F0F0',
            foreground='#666666',
            font=("Consolas", 12)
        )
        self._line_numbers.pack(side='left', fill='y')

        # Bind para actualizar números de línea
        self.bind('<KeyPress>', self._on_key_press)
        self.bind('<KeyRelease>', self.on_key_release)

        # Actualización inicial de números de línea
        self._update_line_numbers()

    def _on_key_press(self, event=None):
        self._update_line_numbers()

    def _update_line_numbers(self):
        # Limpiar números anteriores
        self._line_numbers.delete('1.0', tk.END)

        # Contar líneas en el editor
        count = self.get('1.0', tk.END).count('\n')

        # Generar números de línea
        line_numbers = '\n'.join(str(i).rjust(3) for i in range(1, count + 1))
        self._line_numbers.insert('1.0', line_numbers)

        # Sincronizar scroll
        self._line_numbers.yview_moveto(self.yview()[0])

    def set_callback(self, cb):
        self._callback = cb

    def on_key_release(self, event=None):
        self.highlight_syntax()
        if hasattr(self, "_callback"):
            self._callback()

    def highlight_syntax(self):
        # Remover tags existentes
        for tag in ["comment", "keyword", "identifier", "operator",
                    "number", "string", "error", "error_line", "error_char"]:
            self.tag_remove(tag, "1.0", "end")

        content = self.get("1.0", "end-1c")
        patterns = {
            "comment": r"\$.*$",
            "keyword": r"\b(Num|Text|Bool|If|Else|While|For|Write|Read|True|False)\b",
            "identifier": r"@\w+",
            "operator": r"[=+\-*/<>.]",
            "number": r"\b\d+(\.\d+)?\b",
            "string": r'"[^"]*"'
        }

        for ln, line in enumerate(content.split("\n"), 1):
            for tag, pat in patterns.items():
                for m in re.finditer(pat, line):
                    start, end = f"{ln}.{m.start()}", f"{ln}.{m.end()}"
                    self.tag_add(tag, start, end)

    def highlight_error(self, line, column):
        """Resalta una línea con error y el carácter específico"""
        # Resaltar toda la línea
        self.tag_add("error_line", f"{line}.0", f"{line}.end")

        # Resaltar el carácter específico
        if column is not None:
            self.tag_add("error_char", f"{line}.{column}", f"{line}.{column + 1}")


class LexerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Lexer IDE")

        # Agregar variable para el archivo actual
        self.current_file = None

        # Crear barra de menús
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú "Archivo"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar como...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        # Tema claro
        style = ttk.Style()
        style.configure(".", background="#F5F5F5", foreground="#333333")
        style.configure("Treeview", fieldbackground="#FFFFFF",
                        background="#FFFFFF", foreground="#333333")

        # Grid del root
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=0)  # Nueva columna para el logo
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=3)
        self.root.grid_rowconfigure(2, weight=1)

        self.root.configure(bg="#F5F5F5")

        top_frame = ttk.Frame(self.root)
        top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

        # Menú desplegable de guías (izquierda)
        guide_menu = ttk.Menubutton(top_frame, text="Open Guides", direction="below")
        menu = tk.Menu(guide_menu, tearoff=0)
        menu.add_command(label="Guía Léxica", command=lambda: self.open_pdf("guides/Análisis_léxico.pdf"))
        menu.add_command(label="Guía Sintáctica", command=lambda: self.open_pdf("guides/Análisis_sintáctico.pdf"))
        menu.add_command(label="Guía Semántica", command=lambda: self.open_pdf("guides/Análisis_semántico.pdf"))
        menu.add_command(label="Guía Lenguaje", command=lambda: self.open_pdf("guides/Guia_lenguaje.pdf"))
        guide_menu["menu"] = menu
        guide_menu.pack(side="left", padx=(0, 10))

        # Botón About Us (izquierda)
        about_button = ttk.Button(top_frame, text="About Us", command=self.show_about_us)
        about_button.pack(side="left", padx=(0, 20))

        compiler_frame = ttk.Frame(top_frame)
        compiler_frame.pack(side="left", expand=True, fill="both")

        # Logo del compilador (izquierda del nombre)
        try:
            self.compiler_logo = PhotoImage(file="images/logo_compilador.png")
            self.compiler_logo = self.compiler_logo.subsample(15, 15)
            compiler_logo_label = ttk.Label(compiler_frame, image=self.compiler_logo)
            compiler_logo_label.pack(side="left", expand=True)
        except Exception as e:
            print("No se pudo cargar el logo del compilador:", e)
            ttk.Label(compiler_frame, text="[LOGO]").pack(side="left")

        # Logo (derecha)
        try:
            self.logo_image = PhotoImage(file="images/logo_tecnm.png")
            self.logo_image = self.logo_image.subsample(3, 3)
            logo_label = ttk.Label(top_frame, image=self.logo_image)
            logo_label.pack(side="right", anchor="e")
        except Exception as e:
            print("No se pudo cargar el logo:", e)

        # ── Editor ──────────────────────────────────────────────────────────
        self.code_frame = ttk.LabelFrame(root, text="Code Editor")
        self.code_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Frame para contener el editor y sus números de línea
        editor_container = ttk.Frame(self.code_frame)
        editor_container.pack(expand=True, fill="both", padx=5, pady=5)

        self.code_editor = CustomText(editor_container, wrap=tk.NONE,
                                      bg="#FFFFFF", fg="#333333",
                                      insertbackground="#333333",
                                      font=("Consolas", 12))
        self.code_editor.pack(side="right", expand=True, fill="both")
        self.code_editor.set_callback(self.analyze_code_realtime)

        # Scrollbar para el editor
        code_scroll = ttk.Scrollbar(editor_container, orient="vertical",
                                    command=self._scroll_both)
        code_scroll.pack(side="right", fill="y")
        self.code_editor.configure(yscrollcommand=code_scroll.set)

        # ── Vista de tokens ────────────────────────────────────────────────
        self.token_frame = ttk.LabelFrame(root, text="Tokens")
        self.token_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.token_tree = ttk.Treeview(
            self.token_frame,
            columns=("Type", "Value", "Line", "Column"),
            show="headings"
        )
        for column in ("Type", "Value", "Line", "Column"):
            self.token_tree.heading(column, text=column)
        self.token_tree.pack(expand=True, fill="both", padx=5, pady=5)

        # ── Vista tabla de símbolos ────────────────────────────────────────
        self.sym_frame = ttk.LabelFrame(root, text="Symbol Table")
        self.sym_frame.grid(row=2, column=0, padx=5, pady=5,
                            columnspan=1, sticky="nsew")
        self.sym_tree = ttk.Treeview(
            self.sym_frame,
            columns=("Name", "VarType", "Line"),
            show="headings"
        )
        for column in ("Name", "VarType", "Line"):
            self.sym_tree.heading(column, text=column)
        self.sym_tree.pack(expand=True, fill="both", padx=5, pady=5)

        # ── Vista de errores ───────────────────────────────────────────────
        self.error_frame = ttk.LabelFrame(root, text="Errors")
        self.error_frame.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.error_tree = ttk.Treeview(
            self.error_frame,
            columns=("Type", "Message", "Line", "Column"),
            show="headings"
        )
        for column in ("Type", "Message", "Line", "Column"):
            self.error_tree.heading(column, text=column)
        self.error_tree.pack(expand=True, fill="both", padx=5, pady=5)

    def _scroll_both(self, *args):
        """Sincroniza el scroll del editor y los números de línea"""
        self.code_editor.yview(*args)
        self.code_editor._line_numbers.yview(*args)

    # ───────────────────────── Actualizar GUI ─────────────────────────────
    def analyze_code_realtime(self):
        # Limpiar vistas
        for tree in (self.token_tree, self.sym_tree, self.error_tree):
            tree.delete(*tree.get_children())

        # Obtener código desde el editor y guardarlo temporalmente
        code = self.code_editor.get("1.0", tk.END)
        with open("temp_code.txt", "w", encoding="utf-8") as f:
            f.write(code)

        # Crear nueva tabla de símbolos y nuevo lexer
        symtab = SymbolTable()
        lexer = Lexer("temp_code.txt", symtab)

        # ── Tokens ─────────────────────────────────────────────────────────────
        for tok in symtab.tokens:
            self.token_tree.insert("", tk.END, values=(
                tok.category.value,
                tok.value,
                tok.row,
                tok.column
            ))

        # ── Tabla de Símbolos ──────────────────────────────────────────────────
        for name, info in symtab.all_symbols().items():
            self.sym_tree.insert("", tk.END, values=(
                name,
                info.var_type,
                info.declared_line
            ))

        # ── Errores ÚNICOS ─────────────────────────────────────────────────────
        unique_errors = []
        seen = set()
        for err in lexer.errors.get_all():
            key = (err._type, err._message, err._line, err._column)
            if key not in seen:
                seen.add(key)
                unique_errors.append(err)

        for err in unique_errors:
            self.error_tree.insert("", tk.END, values=(
                err._type,
                err._message,
                err._line,
                err._column
            ))
            self.code_editor.highlight_error(err._line, err._column)

    # ── Abrir archivos de documentación PDF ───────────────────────────────
    def open_pdf(self, filename):
        try:
            filepath = os.path.abspath(filename)
            if os.name == 'nt':  # Windows
                os.startfile(filepath)
            elif sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', filepath])
            else:
                subprocess.Popen(['xdg-open', filepath])
        except Exception as e:
            print("Error al abrir PDF:", e)

    def show_about_us(self):
        about = Toplevel(self.root)
        about.title("About Us")
        about.geometry("400x620")
        about.configure(bg="white")

        info_text = (
            "Proyecto Final - Lenguajes y Autómatas II\n"
            "\nIntegrantes del equipo:\n"
            "• Luis Farid Chaires Pasalagua\n"
            "• José Alfredo Jiménez Téllez\n"
            "• Luis Ruben Rusiles Leal\n"
            "• Oscar Hurtado González\n"
            "\nInstituto Tecnológico de Celaya\n"
        )

        Label(about, text=info_text, justify="left", bg="white", font=("Arial", 11)).pack(pady=10)

        try:
            team_photo = PhotoImage(file="images/Photo_team.png")
            team_photo = team_photo.subsample(7, 7)
            Label(about, image=team_photo, bg="white").pack()
            about.team_photo = team_photo
        except Exception as e:
            print("No se pudo cargar la imagen del equipo:", e)

    # ───────────────────────── Manejo de archivos ─────────────────────────
    def new_file(self):
        """Crear nuevo archivo"""
        self.current_file = None
        self.code_editor.delete(1.0, tk.END)
        self.root.title("Python Lexer IDE - Nuevo archivo")

    def open_file(self):
        """Abrir archivo existente"""
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filepath:
            self.current_file = filepath
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                self.code_editor.delete(1.0, tk.END)
                self.code_editor.insert(1.0, content)
            self.root.title(f"Python Lexer IDE - {filepath}")

    def save_file(self):
        """Guardar archivo actual"""
        if self.current_file:
            content = self.code_editor.get(1.0, tk.END)
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            self.save_as_file()

    def save_as_file(self):
        """Guardar como nuevo archivo"""
        from tkinter import filedialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        if filepath:
            self.current_file = filepath
            content = self.code_editor.get(1.0, tk.END)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            self.root.title(f"Python Lexer IDE - {filepath}")


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    app = LexerGUI(root)
    root.mainloop()