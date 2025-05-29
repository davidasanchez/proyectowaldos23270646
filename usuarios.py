import tkinter as tk
from tkinter import ttk, messagebox
import db

class UsuariosCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Gestión de Usuarios", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Empleado", "Usuario"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")
        self.cargar_usuarios()
        btns = tk.Frame(self.frame)
        btns.pack()
        tk.Button(btns, text="Agregar", command=self.agregar_usuario).pack(side="left", padx=2)
        tk.Button(btns, text="Editar", command=self.editar_usuario).pack(side="left", padx=2)
        tk.Button(btns, text="Eliminar", command=self.eliminar_usuario).pack(side="left", padx=2)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def cargar_usuarios(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("""
            SELECT u.id_usuario, e.nombre, u.username
            FROM usuarios u
            JOIN empleados e ON u.id_empleado = e.id_empleado
        """)
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        con.close()

    def agregar_usuario(self):
        self.formulario_usuario()

    def editar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario")
            return
        datos = self.tree.item(seleccionado[0])["values"]
        self.formulario_usuario(datos)

    def eliminar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un usuario")
            return
        id_usuario = self.tree.item(seleccionado[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario?"):
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
            con.commit()
            con.close()
            self.cargar_usuarios()
            messagebox.showinfo("Éxito", "Usuario eliminado")

    def formulario_usuario(self, datos=None):
        win = tk.Toplevel(self.root)
        win.title("Usuario")
        tk.Label(win, text="Empleado:").grid(row=0, column=0, pady=5, padx=5)
        tk.Label(win, text="Usuario:").grid(row=1, column=0, pady=5, padx=5)
        tk.Label(win, text="Contraseña:").grid(row=2, column=0, pady=5, padx=5)
        combo_emp = ttk.Combobox(win)
        combo_emp.grid(row=0, column=1, pady=5, padx=5)
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_empleado, nombre FROM empleados")
        emps = [f"{e[0]} - {e[1]}" for e in cur.fetchall()]
        con.close()
        combo_emp["values"] = emps
        user = tk.Entry(win)
        user.grid(row=1, column=1, pady=5, padx=5)
        pwd = tk.Entry(win)
        pwd.grid(row=2, column=1, pady=5, padx=5)
        if datos:
            combo_emp.set(f"{datos[0]} - {datos[1]}")
            user.insert(0, datos[2])
        def guardar():
            id_emp = int(combo_emp.get().split(" - ")[0])
            usuario = user.get()
            password = pwd.get()
            con = db.crear_conexion()
            cur = con.cursor()
            if datos:
                cur.execute("UPDATE usuarios SET id_empleado=%s, username=%s, password=%s WHERE id_usuario=%s",
                            (id_emp, usuario, password, datos[0]))
            else:
                cur.execute("INSERT INTO usuarios (id_empleado, username, password) VALUES (%s,%s,%s)",
                            (id_emp, usuario, password))
            con.commit()
            con.close()
            win.destroy()
            self.cargar_usuarios()
            messagebox.showinfo("Éxito", "Usuario guardado")
        tk.Button(win, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()