import tkinter as tk
from tkinter import ttk, messagebox
import db

class ProveedoresCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Gestión de Proveedores", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Dirección", "Teléfono", "Email"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")
        self.cargar_proveedores()
        btns = tk.Frame(self.frame)
        btns.pack()
        tk.Button(btns, text="Agregar", command=self.agregar_proveedor).pack(side="left", padx=2)
        tk.Button(btns, text="Editar", command=self.editar_proveedor).pack(side="left", padx=2)
        tk.Button(btns, text="Eliminar", command=self.eliminar_proveedor).pack(side="left", padx=2)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def cargar_proveedores(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_proveedor, nombre, direccion, telefono, email FROM proveedores")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        con.close()

    def agregar_proveedor(self):
        self.formulario_proveedor()

    def editar_proveedor(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un proveedor")
            return
        datos = self.tree.item(seleccionado[0])["values"]
        self.formulario_proveedor(datos)

    def eliminar_proveedor(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un proveedor")
            return
        id_proveedor = self.tree.item(seleccionado[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proveedor?"):
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("DELETE FROM proveedores WHERE id_proveedor=%s", (id_proveedor,))
            con.commit()
            con.close()
            self.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor eliminado")

    def formulario_proveedor(self, datos=None):
        win = tk.Toplevel(self.root)
        win.title("Proveedor")
        labels = ["Nombre", "Dirección", "Teléfono", "Email"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=i, column=0, pady=5, padx=5)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1, pady=5, padx=5)
            entries.append(entry)
        if datos:
            for i, ent in enumerate(entries):
                ent.insert(0, datos[i+1])
        def guardar():
            nombre = entries[0].get()
            direccion = entries[1].get()
            telefono = entries[2].get()
            email = entries[3].get()
            con = db.crear_conexion()
            cur = con.cursor()
            if datos:
                cur.execute("UPDATE proveedores SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE id_proveedor=%s",
                            (nombre, direccion, telefono, email, datos[0]))
            else:
                cur.execute("INSERT INTO proveedores (nombre, direccion, telefono, email) VALUES (%s,%s,%s,%s)",
                            (nombre, direccion, telefono, email))
            con.commit()
            con.close()
            win.destroy()
            self.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor guardado")
        tk.Button(win, text="Guardar", command=guardar).grid(row=4, column=0, columnspan=2, pady=10)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()