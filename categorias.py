import tkinter as tk
from tkinter import ttk, messagebox
import db

class CategoriasCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Gestión de Categorías", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")
        self.cargar_categorias()
        btns = tk.Frame(self.frame)
        btns.pack()
        tk.Button(btns, text="Agregar", command=self.agregar_categoria).pack(side="left", padx=2)
        tk.Button(btns, text="Editar", command=self.editar_categoria).pack(side="left", padx=2)
        tk.Button(btns, text="Eliminar", command=self.eliminar_categoria).pack(side="left", padx=2)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def cargar_categorias(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_categoria, nombre FROM categorias")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        con.close()

    def agregar_categoria(self):
        self.formulario_categoria()

    def editar_categoria(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una categoría")
            return
        datos = self.tree.item(seleccionado[0])["values"]
        self.formulario_categoria(datos)

    def eliminar_categoria(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una categoría")
            return
        id_categoria = self.tree.item(seleccionado[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta categoría?"):
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("DELETE FROM categorias WHERE id_categoria=%s", (id_categoria,))
            con.commit()
            con.close()
            self.cargar_categorias()
            messagebox.showinfo("Éxito", "Categoría eliminada")

    def formulario_categoria(self, datos=None):
        win = tk.Toplevel(self.root)
        win.title("Categoría")
        tk.Label(win, text="Nombre").grid(row=0, column=0, pady=5, padx=5)
        nombre = tk.Entry(win)
        nombre.grid(row=0, column=1, pady=5, padx=5)
        if datos:
            nombre.insert(0, datos[1])
        def guardar():
            nom = nombre.get()
            con = db.crear_conexion()
            cur = con.cursor()
            if datos:
                cur.execute("UPDATE categorias SET nombre=%s WHERE id_categoria=%s", (nom, datos[0]))
            else:
                cur.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nom,))
            con.commit()
            con.close()
            win.destroy()
            self.cargar_categorias()
            messagebox.showinfo("Éxito", "Categoría guardada")
        tk.Button(win, text="Guardar", command=guardar).grid(row=1, column=0, columnspan=2, pady=10)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()