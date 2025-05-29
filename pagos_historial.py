import tkinter as tk
from tkinter import ttk
import db

class PagosHistorialWindow:
    def __init__(self, root, main_menu=None):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Historial de Pagos", font=("Arial", 16)).pack(pady=10)
        tree = ttk.Treeview(
            self.frame,
            columns=("ID Pago", "ID Venta", "Método de Pago", "Monto", "Fecha de Pago"),
            show="headings"
        )
        for col in ("ID Pago", "ID Venta", "Método de Pago", "Monto", "Fecha de Pago"):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill="both")
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("""SELECT id_pago, id_venta, metodo_pago, monto, fecha_pago FROM pagos ORDER BY fecha_pago DESC""")
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        con.close()
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=8)

    def volver(self):
        self.frame.destroy()
        if self.main_menu:
            self.main_menu.frame.pack()