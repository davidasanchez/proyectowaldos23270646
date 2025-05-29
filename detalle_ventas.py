import tkinter as tk
from tkinter import ttk
import db

class DetalleVentasCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Detalle de Ventas", font=("Arial", 16)).pack(pady=10)
        self.ver_ventas()
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def ver_ventas(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        tree = ttk.Treeview(self.frame, columns=("ID Detalle", "ID Venta", "Producto", "Cantidad", "Precio Unitario", "Subtotal"), show="headings")
        for col in ("ID Detalle", "ID Venta", "Producto", "Cantidad", "Precio Unitario", "Subtotal"):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill="both")

        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("""SELECT d.id_detalle, d.id_venta, p.nombre, d.cantidad, d.precio_unitario, d.subtotal
                       FROM detalle_ventas d
                       JOIN productos p ON d.id_producto = p.id_producto
                       ORDER BY d.id_detalle DESC""")
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        con.close()

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()