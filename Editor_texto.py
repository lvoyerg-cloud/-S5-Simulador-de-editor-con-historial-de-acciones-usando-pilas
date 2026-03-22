import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

# =========================
# CLASE STACK FEEBACK
# =========================
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0


# =========================
# LÓGICA DEL EDITOR
# =========================
class TextEditor:
    def __init__(self):
        self.content = ""
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self._history = []

    def write(self, text):
        if not text or not text.strip():
            raise ValueError("No se puede escribir texto vacío")

        text_to_add = " " + text if self.content and not self.content.endswith(" ") else text

        self.undo_stack.push(("write", text_to_add))
        self.redo_stack = Stack()

        self.content += text_to_add
        self._history.append(f"Escribió: '{text_to_add}'")

    def delete(self, n):
        if n <= 0:
            raise ValueError("El número debe ser mayor que 0")

        if n > len(self.content):
            n = len(self.content)

        deleted = self.content[-n:]
        self.undo_stack.push(("delete", deleted))
        self.redo_stack = Stack()

        self.content = self.content[:-n]
        self._history.append(f"Borró {n} caracteres: '{deleted}'")

    def delete_letter(self, letter):
        if not letter or len(letter) != 1:
            raise ValueError("Ingrese solo una letra")

        original = self.content
        new_content = self.content.replace(letter, "")

        if original == new_content:
            raise ValueError("La letra no existe en el texto")

        self.undo_stack.push(("delete_letter", original))
        self.redo_stack = Stack()

        self.content = new_content
        self._history.append(f"Borró letra: '{letter}'")

    def undo(self):
        if self.undo_stack.is_empty():
            raise IndexError("Nada que deshacer")

        action, value = self.undo_stack.pop()

        if action == "write":
            self.content = self.content[:-len(value)]
            self.redo_stack.push(("write", value))

        elif action == "delete":
            self.content += value
            self.redo_stack.push(("delete", value))

        elif action == "delete_letter":
            self.redo_stack.push(("delete_letter", self.content))
            self.content = value

        self._history.append("Undo realizado")

    def redo(self):
        if self.redo_stack.is_empty():
            raise IndexError("Nada que rehacer")

        action, value = self.redo_stack.pop()

        if action == "write":
            self.content += value
            self.undo_stack.push(("write", value))

        elif action == "delete":
            self.content = self.content[:-len(value)]
            self.undo_stack.push(("delete", value))

        elif action == "delete_letter":
            self.delete_letter(value)

        self._history.append("Redo realizado")

    def show(self):
        return self.content

    def history(self):
        return self._history


# =========================
# INTERFAZ GRÁFICA
# =========================
class TextEditorGUI:
    def __init__(self, root):
        self.editor = TextEditor()
        self.root = root

        self.root.title("Editor Profesional Pro")
        self.root.geometry("720x550")
        self.root.configure(bg="#f5f5f5")

        self.text_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=70, height=12,
            font=("Segoe UI", 12), state=tk.DISABLED
        )
        self.text_area.pack(pady=20)

        frame = tk.Frame(root, bg="#f5f5f5")
        frame.pack(pady=10)

        btn_style = {"width": 12, "padx": 5}

        tk.Button(frame, text="Escribir", command=self.write_text, **btn_style).grid(row=0, column=0)
        tk.Button(frame, text="Borrar", command=self.delete_text, **btn_style).grid(row=0, column=1)
        tk.Button(frame, text="Deshacer", command=self.undo_action, **btn_style).grid(row=0, column=2)
        tk.Button(frame, text="Rehacer", command=self.redo_action, **btn_style).grid(row=0, column=3)

        tk.Button(frame, text="Ver Historial", command=self.show_history, width=15).grid(row=1, column=1, pady=15)
        tk.Button(frame, text="Ver Contenido", command=self.show_content, width=15).grid(row=1, column=2, pady=15)

        tk.Button(root, text="SALIR", command=self.exit_app,
                  width=20, bg="#ff4d4d", fg="white",
                  font=("Arial", 10, "bold")).pack(pady=20)

    def write_text(self):
        text = simpledialog.askstring("Escribir", "Ingrese texto:")
        if text:
            try:
                self.editor.write(text)
                self.update_display()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def delete_text(self):
        opcion = simpledialog.askstring(
            "Tipo de borrado",
            "Escriba:\n1 = Borrar caracteres\n2 = Borrar letra"
        )

        if opcion == "1":
            entry = simpledialog.askstring("Borrar", "Cantidad de caracteres:")
            if entry:
                try:
                    if not entry.isdigit():
                        raise ValueError("Debe ingresar un número válido")

                    self.editor.delete(int(entry))
                    self.update_display()

                except ValueError as e:
                    messagebox.showerror("Error", str(e))

        elif opcion == "2":
            letra = simpledialog.askstring("Borrar letra", "Ingrese una letra:")
            if letra:
                try:
                    self.editor.delete_letter(letra)
                    self.update_display()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

        else:
            messagebox.showinfo("Aviso", "Opción no válida")

    def undo_action(self):
        try:
            self.editor.undo()
            self.update_display()
        except IndexError as e:
            messagebox.showinfo("Undo", str(e))

    def redo_action(self):
        try:
            self.editor.redo()
            self.update_display()
        except IndexError as e:
            messagebox.showinfo("Redo", str(e))

    def show_history(self):
        hist = self.editor.history()
        messagebox.showinfo("Historial", "\n".join(hist[::-1]) if hist else "Sin historial")

    def show_content(self):
        messagebox.showinfo("Contenido", self.editor.show())

    def update_display(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, self.editor.show())
        self.text_area.config(state=tk.DISABLED)

    def exit_app(self):
        if messagebox.askyesno("Salir", "¿Desea cerrar el editor?"):
            self.root.destroy()


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorGUI(root)
    root.mainloop()
