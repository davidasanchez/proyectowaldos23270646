import tkinter as tk
from tkinter import ttk, messagebox
import db

class EmpleadosCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Gestión de Empleados", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Cargo", "Salario"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")
        self.cargar_empleados()
        btns = tk.Frame(self.frame)
        btns.pack()
        tk.Button(btns, text="Agregar", command=self.agregar_empleado).pack(side="left", padx=2)
        tk.Button(btns, text="Editar", command=self.editar_empleado).pack(side="left", padx=2)
        tk.Button(btns, text="Eliminar", command=self.eliminar_empleado).pack(side="left", padx=2)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def cargar_empleados(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_empleado, nombre, cargo, salario FROM empleados")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        con.close()

    def agregar_empleado(self):
        self.formulario_empleado()

    def editar_empleado(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un empleado")
            return
        datos = self.tree.item(seleccionado[0])["values"]
        self.formulario_empleado(datos)

    def eliminar_empleado(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un empleado")
            return
        id_empleado = self.tree.item(seleccionado[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este empleado?"):
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("DELETE FROM empleados WHERE id_empleado=%s", (id_empleado,))
            con.commit()
            con.close()
            self.cargar_empleados()
            messagebox.showinfo("Éxito", "Empleado eliminado")

    def formulario_empleado(self, datos=None):
        win = tk.Toplevel(self.root)
        win.title("Empleado")
        labels = ["Nombre", "Cargo", "Salario"]
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
            cargo = entries[1].get()
            salario = entries[2].get()
            con = db.crear_conexion()
            cur = con.cursor()
            if datos:
                cur.execute("UPDATE empleados SET nombre=%s, cargo=%s, salario=%s WHERE id_empleado=%s",
                            (nombre, cargo, salario, datos[0]))
            else:
                cur.execute("INSERT INTO empleados (nombre, cargo, salario) VALUES (%s,%s,%s)",
                            (nombre, cargo, salario))
            con.commit()
            con.close()
            win.destroy()
            self.cargar_empleados()
            messagebox.showinfo("Éxito", "Empleado guardado")
        tk.Button(win, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()