import tkinter as tk
from tkinter import ttk, messagebox
import db

class ProductosCRUD:
    def __init__(self, root, main_menu, highlight_ids=None):
        self.root = root
        self.main_menu = main_menu
        self.highlight_ids = highlight_ids or []
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Gestión de Productos", font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Precio", "Stock", "Categoría", "Proveedor", "Unidad", "Código Barras"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")
        self.cargar_productos()

        btns = tk.Frame(self.frame)
        btns.pack()
        tk.Button(btns, text="Editar", command=self.editar_producto).pack(side="left", padx=2)
        tk.Button(btns, text="Eliminar", command=self.eliminar_producto).pack(side="left", padx=2)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

    def cargar_productos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("""
            SELECT p.id_producto, p.nombre, p.precio, p.stock, c.nombre, pr.nombre, u.nombre, p.codigo_barras
            FROM productos p
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
            LEFT JOIN unidades u ON p.id_unidad = u.id_unidad
        """)
        for row in cur.fetchall():
            iid = self.tree.insert("", "end", values=row)
            if row[0] in self.highlight_ids:
                self.tree.selection_add(iid)
                self.tree.see(iid)
        con.close()

    def editar_producto(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un producto para editar")
            return
        datos = self.tree.item(seleccionado[0])["values"]
        self.formulario_editar_producto(datos)

    def eliminar_producto(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un producto")
            return
        id_producto = self.tree.item(seleccionado[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
            cur.execute("DELETE FROM inventario WHERE id_producto=%s", (id_producto,))
            con.commit()
            con.close()
            self.cargar_productos()
            messagebox.showinfo("Éxito", "Producto eliminado")

    def formulario_editar_producto(self, datos):
        win = tk.Toplevel(self.root)
        win.title("Editar Producto")
        labels = ["Nombre", "Precio", "Stock", "Categoría", "Proveedor", "Unidad", "Código Barras"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=i, column=0, pady=5, padx=5)
            entry = tk.Entry(win)
            entry.grid(row=i, column=1, pady=5, padx=5)
            entry.insert(0, datos[i+1])  # Salta el ID
            if label not in ["Precio", "Código Barras"]:
                entry.config(state="readonly")
            entries.append(entry)
        def guardar():
            precio = entries[1].get()
            codigo_barras = entries[6].get()
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("""
                UPDATE productos SET precio=%s, codigo_barras=%s WHERE id_producto=%s
            """, (precio, codigo_barras, datos[0]))
            con.commit()
            con.close()
            win.destroy()
            self.cargar_productos()
            messagebox.showinfo("Éxito", "Producto actualizado")
        tk.Button(win, text="Guardar", command=guardar).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()