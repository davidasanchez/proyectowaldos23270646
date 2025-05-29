import tkinter as tk
from tkinter import ttk, messagebox
import db
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class PagosCRUD:
    def __init__(self, root, main_menu, id_venta):
        self.root = root
        self.main_menu = main_menu
        self.id_venta = id_venta
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")
        self.pagos = []

        tk.Label(self.frame, text="Registrar Pago", font=("Arial", 16)).pack(pady=10)

        venta = self.obtener_info_venta()
        self.venta = venta
        if venta:
            datos = f"Cliente: {venta['cliente']}\nTotal: ${venta['total']:.2f}"
            tk.Label(self.frame, text=datos, font=("Arial", 12)).pack()

        pago_frame = tk.Frame(self.frame)
        pago_frame.pack(pady=10)

        tk.Label(pago_frame, text="Método:").grid(row=0, column=0)
        self.metodo_var = tk.StringVar(value="efectivo")
        metodos = ["efectivo", "transferencia", "tarjeta"]
        self.combo_metodo = ttk.Combobox(pago_frame, values=metodos, textvariable=self.metodo_var, state="readonly")
        self.combo_metodo.grid(row=0, column=1)

        tk.Label(pago_frame, text="Monto:").grid(row=0, column=2)
        self.monto_entry = tk.Entry(pago_frame, width=10)
        self.monto_entry.grid(row=0, column=3)

        tk.Button(pago_frame, text="Agregar Pago", command=self.agregar_pago).grid(row=0, column=4, padx=5)

        self.tree = ttk.Treeview(self.frame, columns=("Método", "Monto"), show="headings", height=4)
        for c in ("Método", "Monto"):
            self.tree.heading(c, text=c)
        self.tree.pack(pady=5)

        self.label_total_pagado = tk.Label(self.frame, text="Total pagado: $0.00")
        self.label_total_pagado.pack()
        self.label_cambio = tk.Label(self.frame, text="Cambio: $0.00")
        self.label_cambio.pack()

        self.boton_facturar = None

        tk.Button(self.frame, text="Volver al menú", command=self.volver).pack(pady=10)

    def obtener_info_venta(self):
        con = db.crear_conexion()
        cur = con.cursor()
        cur.execute("""SELECT v.total, c.nombre, c.direccion, c.telefono, c.email
                       FROM ventas v
                       LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
                       WHERE v.id_venta = %s""", (self.id_venta,))
        row = cur.fetchone()
        cur.execute("""SELECT dv.cantidad, p.nombre, dv.precio_unitario
                       FROM detalle_ventas dv
                       JOIN productos p ON dv.id_producto = p.id_producto
                       WHERE dv.id_venta = %s""", (self.id_venta,))
        productos = cur.fetchall()
        con.close()
        if row:
            return {
                "total": float(row[0]),
                "cliente": row[1] or "",
                "direccion": row[2] or "",
                "telefono": row[3] or "",
                "email": row[4] or "",
                "productos": productos
            }
        return None

    def agregar_pago(self):
        metodo = self.metodo_var.get()
        try:
            monto = float(self.monto_entry.get())
            if monto <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Ingrese un monto válido.")
            return

        # Guardar pago en la base de datos
        try:
            con = db.crear_conexion()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO pagos (id_venta, metodo_pago, monto, fecha_pago) VALUES (%s, %s, %s, %s)",
                (self.id_venta, metodo, monto, datetime.now())
            )
            con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror("Error BD", f"Error al guardar el pago en historial: {e}")

        self.pagos.append((metodo, monto))
        self.tree.insert("", "end", values=(metodo, f"${monto:.2f}"))
        self.actualizar_totales()
        self.monto_entry.delete(0, tk.END)

    def actualizar_totales(self):
        total_pagado = sum(m for _, m in self.pagos)
        self.label_total_pagado.config(text=f"Total pagado: ${total_pagado:.2f}")

        total_venta = self.venta["total"]
        cambio = total_pagado - total_venta if total_pagado > total_venta else 0.0
        self.label_cambio.config(text=f"Cambio: ${cambio:.2f}")

        if total_pagado >= total_venta and self.boton_facturar is None:
            self.boton_facturar = tk.Button(self.frame, text="Facturar", command=self.mostrar_factura)
            self.boton_facturar.pack(pady=10)
        elif total_pagado < total_venta and self.boton_facturar:
            self.boton_facturar.destroy()
            self.boton_facturar = None

    def mostrar_factura(self):
        FacturaWindow(self.root, self.venta, self.pagos, self.main_menu, self.frame)

    def volver(self):
        self.frame.destroy()
        self.main_menu.frame.pack()


class FacturaWindow:
    def __init__(self, root, venta, pagos, main_menu, frame_padre):
        self.root = root
        self.venta = venta
        self.pagos = pagos
        self.main_menu = main_menu
        self.frame_padre = frame_padre

        win = tk.Toplevel(root)
        win.title("Factura")
        text = tk.Text(win, width=55, height=25, font=("Courier", 10))
        text.pack()

        # --- Datos del cliente ---
        if venta['cliente'].strip().lower() == "cliente general":
            nombre = direccion = telefono = email = ""
        else:
            nombre = venta['cliente'] or ""
            direccion = venta['direccion'] or ""
            telefono = venta['telefono'] or ""
            email = venta['email'] or ""

        text.insert(tk.END, f"======== FACTURA ========\n")
        text.insert(tk.END, f"Cliente: {nombre}\n")
        if direccion: text.insert(tk.END, f"Dirección: {direccion}\n")
        if telefono: text.insert(tk.END, f"Teléfono: {telefono}\n")
        if email: text.insert(tk.END, f"Email: {email}\n")
        text.insert(tk.END, "\n")
        text.insert(tk.END, f"{'Producto':<18}{'Cant':>5}{'P.U.':>8}{'Sub.':>8}\n")
        total = venta["total"]
        for cant, nombre_prod, precio in venta["productos"]:
            subtotal = float(cant) * float(precio)
            text.insert(tk.END, f"{nombre_prod:<18}{str(cant):>5}{float(precio):>8.2f}{subtotal:>8.2f}\n")

        text.insert(tk.END, "\n")
        text.insert(tk.END, f"{'Total:':<25}${total:.2f}\n")

        # Mostrar los métodos de pago y montos en el preview
        text.insert(tk.END, "Métodos de pago:\n")
        total_pagado = 0
        for metodo, monto in pagos:
            text.insert(tk.END, f"- {metodo.capitalize()}: ${float(monto):.2f}\n")
            total_pagado += float(monto)
        text.insert(tk.END, f"Total pagado: ${total_pagado:.2f}\n")
        cambio = total_pagado - total
        if cambio > 0:
            text.insert(tk.END, f"Cambio: ${cambio:.2f}\n")

        opt_frame = tk.Frame(win)
        opt_frame.pack(pady=5)
        tk.Label(opt_frame, text="¿Desea generar factura electrónica PDF?").pack()
        tk.Button(opt_frame, text="Sí, generar factura PDF", command=lambda: self.generar_factura_pdf(win)).pack(side="left", padx=10)
        tk.Button(opt_frame, text="No, solo cerrar", command=win.destroy).pack(side="left", padx=10)

    def generar_factura_pdf(self, win):
        from datetime import datetime
        import os

        # Guardar en la carpeta 'facturas' del proyecto
        project_path = os.path.dirname(os.path.abspath(__file__))
        facturas_path = os.path.join(project_path, "facturas")
        os.makedirs(facturas_path, exist_ok=True)
        file_name = f"factura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        full_path = os.path.join(facturas_path, file_name)

        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(full_path, pagesize=letter)
        width, height = letter

        # --- Datos del cliente ---
        if self.venta['cliente'].strip().lower() == "cliente general":
            nombre = direccion = telefono = email = ""
        else:
            nombre = self.venta['cliente'] or ""
            direccion = self.venta['direccion'] or ""
            telefono = self.venta['telefono'] or ""
            email = self.venta['email'] or ""

        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height - 50, "FACTURA")
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height - 80, f"Cliente: {nombre}")
        y = height - 100
        if direccion:
            c.drawCentredString(width/2, y, f"Dirección: {direccion}")
            y -= 20
        if telefono:
            c.drawCentredString(width/2, y, f"Teléfono: {telefono}")
            y -= 20
        if email:
            c.drawCentredString(width/2, y, f"Email: {email}")
            y -= 20
        c.drawCentredString(width/2, y, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        y -= 30

        # Tabla de productos centrada
        c.setFont("Helvetica-Bold", 10)
        c.drawString(90, y, "Producto")
        c.drawString(250, y, "Cant")
        c.drawString(300, y, "P.U.")
        c.drawString(370, y, "Sub.")
        y -= 15

        c.setFont("Helvetica", 10)
        for cant, nombre_prod, precio in self.venta["productos"]:
            subtotal = float(cant) * float(precio)
            c.drawString(90, y, str(nombre_prod))
            c.drawRightString(290, y, str(cant))
            c.drawRightString(350, y, f"{float(precio):.2f}")
            c.drawRightString(430, y, f"{subtotal:.2f}")
            y -= 14

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(430, y, f"Total: ${self.venta['total']:.2f}")
        y -= 18

        # Métodos de pago y montos
        c.setFont("Helvetica-Bold", 11)
        c.drawString(90, y, "Métodos de pago:")
        y -= 15
        c.setFont("Helvetica", 10)
        total_pagado = 0
        for metodo, monto in self.pagos:
            c.drawString(110, y, f"- {metodo.capitalize()}: ${float(monto):.2f}")
            total_pagado += float(monto)
            y -= 13

        # Mostrar total pagado y cambio si aplica
        c.setFont("Helvetica-Bold", 11)
        c.drawString(90, y, f"Total pagado: ${total_pagado:.2f}")
        y -= 15
        cambio = total_pagado - self.venta['total']
        if cambio > 0:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(90, y, f"Cambio: ${cambio:.2f}")
            y -= 15

        c.save()
        from tkinter import messagebox
        messagebox.showinfo("Factura PDF", f"Factura generada como\n{full_path}")
        win.destroy()
        self.frame_padre.destroy()
        self.main_menu.frame.pack()