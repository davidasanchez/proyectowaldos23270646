import tkinter as tk
from tkinter import ttk, messagebox
import db
from productos import ProductosCRUD

class ComprasCRUD:
    def __init__(self, root, main_menu):
        self.root = root
        self.main_menu = main_menu
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")

        tk.Label(self.frame, text="Registrar Compra", font=("Arial", 16)).pack(pady=10)

        # Proveedor
        tk.Label(self.frame, text="Proveedor:").pack()
        self.combo_proveedor = ttk.Combobox(self.frame, state="readonly")
        self.combo_proveedor.pack()
        self.cargar_proveedores()

        # Categoría para la compra
        tk.Label(self.frame, text="Categoría de la compra:").pack()
        self.combo_categoria = ttk.Combobox(self.frame, state="readonly")
        self.combo_categoria.pack()
        self.cargar_categorias()

        # Unidad para la compra
        tk.Label(self.frame, text="Unidad de la compra:").pack()
        self.combo_unidad = ttk.Combobox(self.frame, state="readonly")
        self.combo_unidad.pack()
        self.cargar_unidades()

        frm = tk.Frame(self.frame)
        frm.pack()

        tk.Label(frm, text="Producto existente:").grid(row=0, column=0)
        self.combo_producto = ttk.Combobox(frm, width=30, state="readonly")
        self.combo_producto.grid(row=0, column=1)
        self.cargar_productos()

        tk.Button(frm, text="Agregar nuevo producto", command=self.agregar_nuevo_producto).grid(row=0, column=2, padx=10)
        tk.Button(frm, text="Agregar a compra", command=self.agregar_a_tabla).grid(row=1, column=4, padx=5)

        columns = ("ID", "Producto", "Cantidad", "Precio Compra", "Subtotal", "nuevo", "Proveedor", "Categoría", "Unidad")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns[:-4]:
            self.tree.heading(col, text=col)
        self.tree["displaycolumns"] = columns[:-4]
        self.tree.pack(expand=True, fill="both")

        self.total_var = tk.StringVar(value="0.00")
        tk.Label(self.frame, text="Total: $").pack()
        tk.Label(self.frame, textvariable=self.total_var, font=("Arial", 16)).pack()

        btns = tk.Frame(self.frame)
        btns.pack()
        tk.Button(btns, text="Finalizar compra", command=self.finalizar_compra).pack(side="left", padx=2)
        tk.Button(btns, text="Eliminar producto", command=self.eliminar_producto).pack(side="left", padx=2)
        tk.Button(btns, text="Ver Compras", command=self.ver_historial_compras).pack(side="left", padx=2)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

        self.productos_cache = []
        self.cargar_productos_cache()
        self.proveedores_list = []
        self.categorias_list = []
        self.unidades_list = []
        self.cargar_listas_auxiliares()
        self.nuevos_ids = []
        self.editados_ids = []

    def cargar_proveedores(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_proveedor, nombre FROM proveedores")
        proveedores = [f"{c[0]} - {c[1]}" for c in cur.fetchall() if c[1]]
        self.combo_proveedor["values"] = proveedores
        con.close()
        if proveedores:
            self.combo_proveedor.set(proveedores[0])

    def cargar_categorias(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_categoria, nombre FROM categorias")
        categorias = [f"{c[0]} - {c[1]}" for c in cur.fetchall() if c[1]]
        self.combo_categoria["values"] = categorias
        con.close()
        if categorias:
            self.combo_categoria.set(categorias[0])

    def cargar_unidades(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_unidad, nombre FROM unidades")
        unidades = [f"{u[0]} - {u[1]}" for u in cur.fetchall() if u[1]]
        self.combo_unidad["values"] = unidades
        con.close()
        if unidades:
            self.combo_unidad.set(unidades[0])

    def cargar_productos(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_producto, nombre FROM productos")
        productos = [f"{p[0]} - {p[1]}" for p in cur.fetchall() if p[1]]
        self.combo_producto["values"] = productos
        con.close()
        if productos:
            self.combo_producto.set(productos[0])

    def cargar_productos_cache(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_producto, nombre, precio, stock, codigo_barras FROM productos")
        self.productos_cache = cur.fetchall()
        con.close()

    def cargar_listas_auxiliares(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_proveedor, nombre FROM proveedores")
        self.proveedores_list = cur.fetchall()
        cur.execute("SELECT id_categoria, nombre FROM categorias")
        self.categorias_list = cur.fetchall()
        cur.execute("SELECT id_unidad, nombre FROM unidades")
        self.unidades_list = cur.fetchall()
        con.close()

    def buscar_producto_por_nombre(self, nombre):
        for prod in self.productos_cache:
            if prod[1].strip().lower() == nombre.strip().lower():
                return prod
        return None

    def agregar_nuevo_producto(self):
        win = tk.Toplevel(self.root)
        win.title("Agregar Nuevo Producto")
        win.grab_set()

        tk.Label(win, text="Nombre:").grid(row=0, column=0, sticky="e")
        nombre_entry = tk.Entry(win)
        nombre_entry.grid(row=0, column=1)

        tk.Label(win, text="Stock inicial:").grid(row=1, column=0, sticky="e")
        stock_entry = tk.Entry(win)
        stock_entry.grid(row=1, column=1)

        tk.Label(win, text="Precio compra:").grid(row=2, column=0, sticky="e")
        precio_entry = tk.Entry(win)
        precio_entry.grid(row=2, column=1)

        tk.Label(win, text="Proveedor:").grid(row=3, column=0, sticky="e")
        combo_prov = ttk.Combobox(win, state="readonly", values=[f"{p[0]} - {p[1]}" for p in self.proveedores_list])
        combo_prov.grid(row=3, column=1)
        if self.proveedores_list:
            combo_prov.set(f"{self.proveedores_list[0][0]} - {self.proveedores_list[0][1]}")

        tk.Label(win, text="Categoría:").grid(row=4, column=0, sticky="e")
        combo_cat = ttk.Combobox(win, state="readonly", values=[f"{c[0]} - {c[1]}" for c in self.categorias_list])
        combo_cat.grid(row=4, column=1)
        if self.categorias_list:
            combo_cat.set(f"{self.categorias_list[0][0]} - {self.categorias_list[0][1]}")

        tk.Label(win, text="Unidad:").grid(row=5, column=0, sticky="e")
        combo_uni = ttk.Combobox(win, state="readonly", values=[f"{u[0]} - {u[1]}" for u in self.unidades_list])
        combo_uni.grid(row=5, column=1)
        if self.unidades_list:
            combo_uni.set(f"{self.unidades_list[0][0]} - {self.unidades_list[0][1]}")

        def guardar():
            nombre = nombre_entry.get().strip()
            stock = stock_entry.get().strip()
            precio = precio_entry.get().strip()
            prov = combo_prov.get()
            cat = combo_cat.get()
            uni = combo_uni.get()
            if not nombre or not stock or not precio or not prov or not cat or not uni:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            try:
                stock = int(stock)
                precio = float(precio)
                id_prov = int(prov.split(" - ")[0])
                id_cat = int(cat.split(" - ")[0])
                id_uni = int(uni.split(" - ")[0])
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")
                return

            existente = self.buscar_producto_por_nombre(nombre)
            if existente:
                self.tree.insert("", "end", values=(
                    existente[0], existente[1], stock, precio, stock*precio, False, id_prov, id_cat, id_uni
                ))
                if existente[0] not in self.editados_ids:
                    self.editados_ids.append(existente[0])
            else:
                self.tree.insert("", "end", values=(
                    "", nombre, stock, precio, stock*precio, True, id_prov, id_cat, id_uni
                ))
            self.actualizar_total()
            win.destroy()

        tk.Button(win, text="Añadir", command=guardar).grid(row=6, column=0, columnspan=2, pady=10)

    def agregar_a_tabla(self):
        producto_text = self.combo_producto.get()
        if not producto_text:
            messagebox.showerror("Error", "Seleccione un producto existente.")
            return
        id_producto = int(producto_text.split(" - ")[0])
        producto = next((p for p in self.productos_cache if p[0] == id_producto), None)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        win = tk.Toplevel(self.root)
        win.title("Agregar producto existente a compra")
        win.grab_set()

        tk.Label(win, text="Cantidad:").grid(row=0, column=0, sticky="e")
        cantidad_entry = tk.Entry(win)
        cantidad_entry.grid(row=0, column=1)

        tk.Label(win, text="Precio compra:").grid(row=1, column=0, sticky="e")
        precio_entry = tk.Entry(win)
        precio_entry.insert(0, str(producto[2]))
        precio_entry.grid(row=1, column=1)

        tk.Label(win, text="Proveedor:").grid(row=2, column=0, sticky="e")
        combo_prov = ttk.Combobox(win, state="readonly", values=[f"{p[0]} - {p[1]}" for p in self.proveedores_list])
        combo_prov.grid(row=2, column=1)
        if self.proveedores_list:
            combo_prov.set(f"{self.proveedores_list[0][0]} - {self.proveedores_list[0][1]}")

        tk.Label(win, text="Categoría:").grid(row=3, column=0, sticky="e")
        combo_cat = ttk.Combobox(win, state="readonly", values=[f"{c[0]} - {c[1]}" for c in self.categorias_list])
        combo_cat.grid(row=3, column=1)
        if self.categorias_list:
            combo_cat.set(f"{self.categorias_list[0][0]} - {self.categorias_list[0][1]}")

        tk.Label(win, text="Unidad:").grid(row=4, column=0, sticky="e")
        combo_uni = ttk.Combobox(win, state="readonly", values=[f"{u[0]} - {u[1]}" for u in self.unidades_list])
        combo_uni.grid(row=4, column=1)
        if self.unidades_list:
            combo_uni.set(f"{self.unidades_list[0][0]} - {self.unidades_list[0][1]}")

        def guardar():
            cantidad = cantidad_entry.get().strip()
            precio = precio_entry.get().strip()
            prov = combo_prov.get()
            cat = combo_cat.get()
            uni = combo_uni.get()
            if not cantidad or not precio or not prov or not cat or not uni:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            try:
                cantidad = int(cantidad)
                precio = float(precio)
                id_prov = int(prov.split(" - ")[0])
                id_cat = int(cat.split(" - ")[0])
                id_uni = int(uni.split(" - ")[0])
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")
                return

            subtotal = cantidad * precio
            self.tree.insert("", "end", values=(
                id_producto, producto[1], cantidad, precio, subtotal, False, id_prov, id_cat, id_uni
            ))
            self.actualizar_total()
            if id_producto not in self.editados_ids:
                self.editados_ids.append(id_producto)
            win.destroy()

        tk.Button(win, text="Añadir", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)

    def eliminar_producto(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un producto")
            return
        item = self.tree.item(seleccionado[0])["values"]
        if not item[5] and item[0] in self.editados_ids:
            self.editados_ids.remove(item[0])
        self.tree.delete(seleccionado[0])
        self.actualizar_total()

    def actualizar_total(self):
        total = 0
        for iid in self.tree.get_children():
            total += float(self.tree.item(iid)["values"][4])
        self.total_var.set(str(round(total, 2)))

    def finalizar_compra(self):
        if not self.tree.get_children():
            messagebox.showwarning("Atención", "No hay productos en la compra")
            return
        try:
            id_proveedor = int(self.combo_proveedor.get().split(" - ")[0])
            id_categoria = int(self.combo_categoria.get().split(" - ")[0])
            id_unidad = int(self.combo_unidad.get().split(" - ")[0])
            total = float(self.total_var.get())
            con = db.crear_conexion()
            cur = con.cursor()
            # Ahora el insert incluye id_categoria e id_unidad
            cur.execute("INSERT INTO compras (id_proveedor, total, id_categoria, id_unidad) VALUES (%s, %s, %s, %s)",
                        (id_proveedor, total, id_categoria, id_unidad))
            id_compra = cur.lastrowid

            productos_para_editar = []
            for cont, iid in enumerate(self.tree.get_children()):
                (id_producto, nombre, cantidad, precio, subtotal, es_nuevo, id_prov, id_cat, id_uni) = self.tree.item(iid)["values"]
                if not id_producto or id_producto == "":
                    codigo_temp = f"PENDIENTE-{nombre[:6]}-{cantidad}-{id_compra}-{cont}"
                    cur.execute(
                        "INSERT INTO productos (nombre, precio, stock, id_categoria, id_proveedor, id_unidad, codigo_barras) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (nombre, precio, cantidad, id_cat, id_prov, id_uni, codigo_temp)
                    )
                    nuevo_id = cur.lastrowid
                    productos_para_editar.append(nuevo_id)
                    cur.execute("INSERT INTO inventario (id_producto, cantidad) VALUES (%s, %s)", (nuevo_id, cantidad))
                    cur.execute(
                        "INSERT INTO detalles_compras(id_compra, id_producto, cantidad, precio_unitario, subtotal) VALUES (%s,%s,%s,%s,%s)",
                        (id_compra, nuevo_id, cantidad, precio, subtotal)
                    )
                else:
                    cur.execute("UPDATE productos SET stock = stock + %s WHERE id_producto = %s", (cantidad, id_producto))
                    cur.execute("UPDATE inventario SET cantidad = cantidad + %s WHERE id_producto = %s", (cantidad, id_producto))
                    cur.execute(
                        "INSERT INTO detalles_compras(id_compra, id_producto, cantidad, precio_unitario, subtotal) VALUES (%s,%s,%s,%s,%s)",
                        (id_compra, id_producto, cantidad, precio, subtotal)
                    )
                    if id_producto not in productos_para_editar:
                        productos_para_editar.append(id_producto)

            con.commit()
            messagebox.showinfo("Éxito", f"Compra registrada. ID: {id_compra}")

            for iid in self.tree.get_children():
                self.tree.delete(iid)
            self.actualizar_total()
            self.cargar_productos_cache()
            self.cargar_productos()

            self.frame.destroy()
            if productos_para_editar:
                ProductosCRUD(self.root, self.main_menu, highlight_ids=productos_para_editar)
            else:
                self.main_menu.frame.pack()
        except Exception as e:
            messagebox.showerror("Error", f"No fue posible registrar la compra\n{e}")

    def ver_historial_compras(self):
        HistorialComprasWindow(self.root, self)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()


class HistorialComprasWindow:
    def __init__(self, root, compras_crud):
        self.top = tk.Toplevel(root)
        self.top.title("Historial de Compras")
        tk.Label(self.top, text="Historial de Compras", font=("Arial", 14)).pack(pady=10)

        columns = ("ID Compra", "Fecha", "Proveedor", "Total", "Categoría", "Unidad")
        tree = ttk.Treeview(self.top, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, anchor='center')
        tree.pack(padx=20, pady=5, fill="both", expand=True)

        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute(
            """SELECT c.id_compra, c.fecha, p.nombre, c.total, cat.nombre, u.nombre
               FROM compras c
               JOIN proveedores p ON c.id_proveedor = p.id_proveedor
               LEFT JOIN categorias cat ON c.id_categoria = cat.id_categoria
               LEFT JOIN unidades u ON c.id_unidad = u.id_unidad
               ORDER BY c.fecha DESC"""
        )
        for id_compra, fecha, proveedor, total, categoria, unidad in cur.fetchall():
            fecha_str = fecha.strftime("%d/%m/%Y %H:%M") if fecha else "Sin fecha"
            tree.insert("", "end", values=(
                id_compra, fecha_str, proveedor, f"${float(total):.2f}", categoria, unidad
            ))
        con.close()

        tree.bind("<Double-1>", lambda e: self.ver_detalle_compra(tree))

        tk.Button(self.top, text="Cerrar", command=self.top.destroy).pack(pady=10)

    def ver_detalle_compra(self, tree):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        id_compra = int(values[0])
        DetalleCompraWindow(self.top, id_compra)

class DetalleCompraWindow:
    def __init__(self, root, id_compra):
        self.top = tk.Toplevel(root)
        self.top.title(f"Detalle de Compra #{id_compra}")
        tk.Label(self.top, text=f"Detalle de Compra #{id_compra}", font=("Arial", 14)).pack(pady=10)

        columns = ("Producto", "Cantidad", "Precio Unitario", "Subtotal")
        tree = ttk.Treeview(self.top, columns=columns, show="headings")
        for c in columns:
            tree.heading(c, text=c)
            tree.column(c, anchor='center')
        tree.pack(padx=20, pady=5, fill="both", expand=True)

        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute(
            """SELECT p.nombre, dc.cantidad, dc.precio_unitario, (dc.cantidad * dc.precio_unitario)
               FROM detalles_compras dc
               JOIN productos p ON dc.id_producto = p.id_producto
               WHERE dc.id_compra = %s""", (id_compra,)
        )
        for nombre, cantidad, precio, subtotal in cur.fetchall():
            tree.insert("", "end", values=(
                nombre, cantidad, f"${float(precio):.2f}", f"${float(subtotal):.2f}"
            ))
        con.close()
        tk.Button(self.top, text="Cerrar", command=self.top.destroy).pack(pady=10)