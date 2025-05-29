import tkinter as tk
from tkinter import ttk, messagebox
import db

class UnidadesCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Gestión de Unidades", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")
        self.cargar_unidades()
        btns = tk.Frame(self.frame)
        btns.pack()
        tk.Button(btns, text="Agregar", command=self.agregar_unidad).pack(side="left", padx=2)
        tk.Button(btns, text="Editar", command=self.editar_unidad).pack(side="left", padx=2)
        tk.Button(btns, text="Eliminar", command=self.eliminar_unidad).pack(side="left", padx=2)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def cargar_unidades(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_unidad, nombre FROM unidades")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        con.close()

    def agregar_unidad(self):
        self.formulario_unidad()

    def editar_unidad(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una unidad")
            return
        datos = self.tree.item(seleccionado[0])["values"]
        self.formulario_unidad(datos)

    def eliminar_unidad(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una unidad")
            return
        id_unidad = self.tree.item(seleccionado[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta unidad?"):
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("DELETE FROM unidades WHERE id_unidad=%s", (id_unidad,))
            con.commit()
            con.close()
            self.cargar_unidades()
            messagebox.showinfo("Éxito", "Unidad eliminada")

    def formulario_unidad(self, datos=None):
        win = tk.Toplevel(self.root)
        win.title("Unidad")
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
                cur.execute("UPDATE unidades SET nombre=%s WHERE id_unidad=%s", (nom, datos[0]))
            else:
                cur.execute("INSERT INTO unidades (nombre) VALUES (%s)", (nom,))
            con.commit()
            con.close()
            win.destroy()
            self.cargar_unidades()
            messagebox.showinfo("Éxito", "Unidad guardada")
        tk.Button(win, text="Guardar", command=guardar).grid(row=1, column=0, columnspan=2, pady=10)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()