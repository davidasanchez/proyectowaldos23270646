import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import db
from pagos import PagosCRUD
from datetime import datetime

class VentasCRUD:
    def __init__(self, root, main_menu, usuario=None):
        self.root = root
        self.main_menu = main_menu
        self.usuario = usuario
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Registrar Venta", font=("Arial", 16)).pack(pady=10, anchor="w")

        tk.Button(self.frame, text="Guardar Temporal", command=self.guardar_tabla_temporal).place(relx=1.0, y=10, anchor="ne")
        tk.Button(self.frame, text="Restaurar Temporal", command=self.cargar_tabla_temporal).place(relx=0.8, y=10, anchor="ne")

        tk.Label(self.frame, text="Cliente:").pack()
        self.combo_cliente = ttk.Combobox(self.frame)
        self.combo_cliente.pack()
        self.cargar_clientes()

        buscador_frame = tk.Frame(self.frame)
        buscador_frame.pack()
        tk.Label(buscador_frame, text="Buscar producto:").pack(side="left")
        self.busqueda_entry = tk.Entry(buscador_frame)
        self.busqueda_entry.pack(side="left")
        self.busqueda_entry.bind("<KeyRelease>", self.buscar_producto)
        tk.Button(buscador_frame, text="L. Barras", command=self.leer_codigo_barras).pack(side="left")

        self.lista_resultados = tk.Listbox(self.frame, height=5)
        self.lista_resultados.pack_forget()
        self.lista_resultados.bind("<Double-Button-1>", self.selecciona_producto_lista)
        self.lista_resultados.bind("<Return>", self.selecciona_producto_lista)

        frm = tk.Frame(self.frame)
        frm.pack()
        tk.Label(frm, text="Producto:").grid(row=0, column=0)
        self.combo_producto = ttk.Combobox(frm)
        self.combo_producto.grid(row=0, column=1)
        self.combo_producto.bind("<<ComboboxSelected>>", self.producto_seleccionado)
        self.cargar_productos()

        tk.Label(frm, text="Cantidad:").grid(row=0, column=2)
        self.cant_entry = tk.Entry(frm, width=8)
        self.cant_entry.grid(row=0, column=3)
        tk.Label(frm, text="Precio venta:").grid(row=0, column=4)
        self.precio_entry = tk.Entry(frm, width=10)
        self.precio_entry.grid(row=0, column=5)
        tk.Button(frm, text="Agregar", command=self.agregar_a_tabla).grid(row=0, column=6)

        columns = ("ID", "Producto", "Cantidad", "Precio Venta", "Subtotal")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")

        self.total_var = tk.StringVar(value="0.00")
        tk.Label(self.frame, text="Total: $").pack()
        tk.Label(self.frame, textvariable=self.total_var, font=("Arial", 16)).pack()

        btns = tk.Frame(self.frame)
        btns.pack()
        tk.Button(btns, text="Finalizar venta", command=self.finalizar_venta).pack(side="left", padx=2)
        tk.Button(btns, text="Eliminar producto", command=self.eliminar_producto).pack(side="left", padx=2)
        tk.Button(self.frame, text="Ver Ventas", command=self.ver_ventas).pack(pady=5)
        tk.Button(self.frame, text="Volver", command=self.volver).pack(pady=10)

        self.productos_cache = []
        self.cargar_productos_cache()

    def cargar_clientes(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_cliente, nombre FROM clientes")
        clientes = [f"{c[0]} - {c[1]}" for c in cur.fetchall()]
        self.combo_cliente["values"] = clientes
        con.close()
        if clientes:
            self.combo_cliente.set(clientes[0])

    def cargar_productos(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("SELECT id_producto, nombre FROM productos")
        productos = [f"{p[0]} - {p[1]}" for p in cur.fetchall()]
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

    def buscar_producto(self, event=None):
        texto = self.busqueda_entry.get().lower()
        resultados = [p for p in self.productos_cache if texto and texto in p[1].lower()]
        self.lista_resultados.delete(0, tk.END)
        if resultados:
            for p in resultados:
                self.lista_resultados.insert(tk.END, f"{p[0]} - {p[1]}")
            self.lista_resultados.pack(after=self.busqueda_entry, fill="x")
        else:
            self.lista_resultados.pack_forget()

    def selecciona_producto_lista(self, event=None):
        seleccion = self.lista_resultados.curselection()
        if not seleccion:
            return
        texto = self.lista_resultados.get(seleccion[0])
        id_producto = int(texto.split(" - ")[0])
        producto = next((p for p in self.productos_cache if p[0] == id_producto), None)
        if producto:
            self.combo_producto.set(f"{producto[0]} - {producto[1]}")
            self.precio_entry.delete(0, tk.END)
            self.precio_entry.insert(0, str(producto[2]))
            self.lista_resultados.pack_forget()
            self.busqueda_entry.delete(0, tk.END)

    def producto_seleccionado(self, event=None):
        producto_text = self.combo_producto.get()
        if not producto_text:
            return
        id_producto = int(producto_text.split(" - ")[0])
        producto = next((p for p in self.productos_cache if p[0] == id_producto), None)
        if producto:
            self.precio_entry.delete(0, tk.END)
            self.precio_entry.insert(0, str(producto[2]))

    def leer_codigo_barras(self):
        codigo = simpledialog.askstring("Código de Barras", "Escanee o escriba el código:")
        if not codigo:
            return
        producto = next((p for p in self.productos_cache if p[4] == codigo), None)
        if producto:
            self.combo_producto.set(f"{producto[0]} - {producto[1]}")
            self.precio_entry.delete(0, tk.END)
            self.precio_entry.insert(0, str(producto[2]))
            self.busqueda_entry.delete(0, tk.END)
            self.lista_resultados.pack_forget()
        else:
            messagebox.showerror("No encontrado", "No existe producto con ese código")

    def agregar_a_tabla(self):
        producto_text = self.combo_producto.get()
        if not producto_text:
            messagebox.showerror("Error", "Seleccione un producto.")
            return
        id_producto = int(producto_text.split(" - ")[0])
        producto = next((p for p in self.productos_cache if p[0] == id_producto), None)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
        nombre = producto[1]
        stock = producto[3]
        try:
            cantidad = int(self.cant_entry.get())
            precio = float(self.precio_entry.get())
            if cantidad > stock:
                messagebox.showerror("Error", f"Stock insuficiente.\nStock actual: {stock}")
                return
            subtotal = cantidad * precio
            self.tree.insert("", "end", values=(id_producto, nombre, cantidad, precio, subtotal))
            self.actualizar_total()
        except:
            messagebox.showerror("Error", "Datos inválidos")

    def eliminar_producto(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un producto")
            return
        self.tree.delete(seleccionado[0])
        self.actualizar_total()

    def actualizar_total(self):
        total = 0
        for iid in self.tree.get_children():
            total += float(self.tree.item(iid)["values"][4])
        self.total_var.set(str(round(total, 2)))

    def finalizar_venta(self):
        if not self.tree.get_children():
            messagebox.showwarning("Atención", "No hay productos en la venta")
            return
        try:
            id_cliente = int(self.combo_cliente.get().split(" - ")[0])
            total = float(self.total_var.get())
            id_usuario = self.usuario["id_usuario"] if self.usuario and "id_usuario" in self.usuario else None

            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("INSERT INTO ventas (id_cliente, total, id_usuario) VALUES (%s, %s, %s)", (id_cliente, total, id_usuario))
            id_venta = cur.lastrowid

            for iid in self.tree.get_children():
                id_producto, nombre, cantidad, precio, subtotal = self.tree.item(iid)["values"]
                cur.execute(
                    "INSERT INTO detalle_ventas(id_venta, id_producto, cantidad, precio_unitario, subtotal) VALUES (%s,%s,%s,%s,%s)",
                    (id_venta, id_producto, cantidad, precio, subtotal)
                )
                cur.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (cantidad, id_producto))
                cur.execute("UPDATE inventario SET cantidad = cantidad - %s WHERE id_producto = %s", (cantidad, id_producto))
                cur.execute("SELECT stock FROM productos WHERE id_producto = %s", (id_producto,))
                nuevo_stock = cur.fetchone()
                if nuevo_stock and nuevo_stock[0] <= 0:
                    cur.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))

            con.commit()
            messagebox.showinfo("Éxito", f"Venta registrada. ID: {id_venta}")

            for iid in list(self.tree.get_children()):
                self.tree.delete(iid)
            self.actualizar_total()
            self.cargar_productos_cache()
            self.cargar_productos()

            self.frame.destroy()
            PagosCRUD(self.root, self.main_menu, id_venta)
        except Exception as e:
            messagebox.showerror("Error", f"No fue posible registrar la venta\n{e}")

    # --- FUNCIONES DE VENTA TEMPORAL EN MYSQL ---
    def guardar_tabla_temporal(self):
        if not self.tree.get_children():
            messagebox.showwarning("Atención", "No hay productos para guardar")
            return
        try:
            id_cliente = int(self.combo_cliente.get().split(" - ")[0])
            id_usuario = self.usuario["id_usuario"] if self.usuario and "id_usuario" in self.usuario else None
            total = float(self.total_var.get())

            con = db.crear_conexion()
            cur = con.cursor()
            # Inserta cabecera temporal
            cur.execute("INSERT INTO ventas_temporales (id_usuario, id_cliente, total) VALUES (%s, %s, %s)", (id_usuario, id_cliente, total))
            id_temp = cur.lastrowid

            # Inserta detalle temporal
            for iid in self.tree.get_children():
                id_producto, nombre, cantidad, precio, subtotal = self.tree.item(iid)["values"]
                cur.execute(
                    "INSERT INTO detalle_ventas_temporales (id_temp, id_producto, nombre_producto, cantidad, precio, subtotal) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_temp, id_producto, nombre, cantidad, precio, subtotal)
                )
            con.commit()
            con.close()
            messagebox.showinfo("Guardado", f"Venta temporal guardada.")
            # Limpia la tabla visual
            for iid in list(self.tree.get_children()):
                self.tree.delete(iid)
            self.actualizar_total()
        except Exception as e:
            messagebox.showerror("Error", f"No fue posible guardar la venta temporal\n{e}")

    def cargar_tabla_temporal(self):
        win = tk.Toplevel(self.root)
        win.title("Ventas Temporales")
        tree = ttk.Treeview(win, columns=("ID", "Cliente", "Fecha", "Total"), show="headings")
        for col in ("ID", "Cliente", "Fecha", "Total"):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill="both")
        con = db.crear_conexion()
        cur = con.cursor()
        id_usuario = self.usuario["id_usuario"] if self.usuario and "id_usuario" in self.usuario else None
        cur.execute("""
            SELECT vt.id_temp, c.nombre, vt.fecha, vt.total
            FROM ventas_temporales vt
            JOIN clientes c ON vt.id_cliente = c.id_cliente
            WHERE vt.id_usuario = %s
            ORDER BY vt.fecha DESC
        """, (id_usuario,))
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        con.close()

        def cargar_venta():
            seleccionado = tree.selection()
            if not seleccionado:
                messagebox.showwarning("Atención", "Seleccione una venta temporal")
                return
            id_temp = tree.item(seleccionado[0])["values"][0]

            # Carga detalle y llena la interfaz de venta
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("SELECT id_cliente FROM ventas_temporales WHERE id_temp = %s", (id_temp,))
            cliente_row = cur.fetchone()
            cur.execute("SELECT id_producto, nombre_producto, cantidad, precio, subtotal FROM detalle_ventas_temporales WHERE id_temp = %s", (id_temp,))
            detalles = cur.fetchall()
            con.close()

            # Limpia la UI
            for iid in self.tree.get_children():
                self.tree.delete(iid)
            # Set cliente
            if cliente_row:
                id_cliente = cliente_row[0]
                for val in self.combo_cliente["values"]:
                    if val.startswith(f"{id_cliente} -"):
                        self.combo_cliente.set(val)
                        break
            # Llena detalle
            for det in detalles:
                self.tree.insert("", "end", values=det)
            self.actualizar_total()

            # Borra venta temporal de la base
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute("DELETE FROM detalle_ventas_temporales WHERE id_temp = %s", (id_temp,))
            cur.execute("DELETE FROM ventas_temporales WHERE id_temp = %s", (id_temp,))
            con.commit()
            con.close()
            win.destroy()

        tk.Button(win, text="Cargar venta seleccionada", command=cargar_venta).pack(pady=5)

    def ver_ventas(self):
        VentasHistorialWindow(self.root)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()

class VentasHistorialWindow:
    def __init__(self, root):
        win = tk.Toplevel(root)
        win.title("Historial de Ventas")
        tree = ttk.Treeview(win, columns=("ID", "Cliente", "Total", "Fecha", "Usuario"), show="headings")
        for col in ("ID", "Cliente", "Total", "Fecha", "Usuario"):
            tree.heading(col, text=col)
        tree.pack(expand=True, fill="both")
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("""
            SELECT v.id_venta, c.nombre, v.total, v.fecha, u.username
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
            LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
            ORDER BY v.fecha DESC
        """)
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        con.close()