import tkinter as tk
from productos import ProductosCRUD
from categorias import CategoriasCRUD
from proveedores import ProveedoresCRUD
from clientes import ClientesCRUD
from ventas import VentasCRUD
from compras import ComprasCRUD
from empleados import EmpleadosCRUD
from usuarios import UsuariosCRUD
from inventario import InventarioCRUD
from unidades import UnidadesCRUD
from detalle_compras import DetalleComprasCRUD
from detalle_ventas import DetalleVentasCRUD
from pagos_historial import PagosHistorialWindow  # <--- Importa el historial de pagos

class MainMenu:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)
        tk.Label(self.frame, text=f"Bienvenido {usuario['empleado']}", font=("Arial", 14)).pack(pady=10)
        botones = [
            ("Productos", ProductosCRUD),
            ("Categorías", CategoriasCRUD),
            ("Proveedores", ProveedoresCRUD),
            ("Clientes", ClientesCRUD),
            ("Ventas", VentasCRUD),
            ("Compras", ComprasCRUD),
            ("Empleados", EmpleadosCRUD),
            ("Usuarios", UsuariosCRUD),
            ("Inventario", InventarioCRUD),
            ("Unidades", UnidadesCRUD),
            ("Historial Pagos", PagosHistorialWindow),  # <--- Agrega aquí el historial
            ("Detalle Compras", DetalleComprasCRUD),
            ("Detalle Ventas", DetalleVentasCRUD)
        ]
        for texto, clase in botones:
            tk.Button(self.frame, text=texto, width=25, command=lambda c=clase: self.abrir_modulo(c)).pack(pady=2)
        tk.Button(self.frame, text="Salir", width=25, command=self.root.quit).pack(pady=10)

    def abrir_modulo(self, ClaseModulo):
        self.frame.pack_forget()
        # Pasar usuario a ventas
        if ClaseModulo.__name__ == "VentasCRUD":
            ClaseModulo(self.root, self, self.usuario)
        else:
            ClaseModulo(self.root, self)