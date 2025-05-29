import tkinter as tk
from tkinter import messagebox
import db
from utilidades import MainMenu

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)
        tk.Label(self.frame, text="Usuario").grid(row=0, column=0, pady=10, padx=10)
        tk.Label(self.frame, text="Contraseña").grid(row=1, column=0, pady=10, padx=10)
        self.usuario = tk.Entry(self.frame)
        self.usuario.grid(row=0, column=1)
        self.contrasena = tk.Entry(self.frame, show="*")
        self.contrasena.grid(row=1, column=1)
        tk.Button(self.frame, text="Ingresar", width=20, command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        user = self.usuario.get()
        pwd = self.contrasena.get()
        con = db.crear_conexion()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT u.*, e.nombre as empleado FROM usuarios u JOIN empleados e ON u.id_empleado=e.id_empleado WHERE username=%s AND password=%s", (user, pwd))
        usuario = cur.fetchone()
        con.close()
        if usuario:
            self.frame.destroy()
            MainMenu(self.root, usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")