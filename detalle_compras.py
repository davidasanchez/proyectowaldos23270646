import tkinter as tk
from tkinter import ttk
import db

class DetalleComprasCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Detalle de Compras", font=("Arial", 16)).pack(pady=10)
        self.ver_compras()
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def ver_compras(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        tree = ttk.Treeview(self.frame, columns=("ID", "Proveedor", "Fecha", "Total"), show="headings")
        for col in ("ID", "Proveedor", "Fecha", "Total"):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill="both")

        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT c.id_compra, p.nombre, c.fecha, c.total FROM compras c LEFT JOIN proveedores p ON c.id_proveedor=p.id_proveedor ORDER BY c.fecha DESC")
        compras = cur.fetchall()
        for row in compras:
            iid = tree.insert("", "end", values=row)
            cur.execute("""
                SELECT d.id_producto, pr.nombre, d.cantidad, d.precio_unitario, d.subtotal
                FROM detalles_compras d
                JOIN productos pr ON d.id_producto = pr.id_producto
                WHERE d.id_compra=%s
            """, (row[0],))
            for det in cur.fetchall():
                tree.insert(iid, "end", values=("", f"Producto: {det[1]}", f"Cantidad: {det[2]}", f"PU: {det[3]:.2f} Sub: {det[4]:.2f}"))
        con.close()

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()