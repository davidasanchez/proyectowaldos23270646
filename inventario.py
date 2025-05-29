import tkinter as tk
from tkinter import ttk
import db

class InventarioCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Inventario", font=("Arial", 16)).pack(pady=10)
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Producto", "Cantidad", "Última actualización"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)
        self.cargar_inventario()

    def cargar_inventario(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("""
            SELECT i.id_inventario, p.nombre, i.cantidad, i.fecha_actualizacion
            FROM inventario i JOIN productos p ON i.id_producto = p.id_producto
        """)
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        con.close()

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()