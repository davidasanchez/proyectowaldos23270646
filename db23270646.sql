-- Crear base de datos
CREATE DATABASE IF NOT EXISTS waldos;
USE waldos;

-- Tabla: categorias
CREATE TABLE categorias (
    id_categoria INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla: clientes
CREATE TABLE clientes (
    id_cliente INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(50),
    email VARCHAR(100)
);

-- Tabla: proveedores
CREATE TABLE proveedores (
    id_proveedor INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(50),
    email VARCHAR(100)
);

-- Tabla: unidades
CREATE TABLE unidades (
    id_unidad INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla: productos
CREATE TABLE productos (
    id_producto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_categoria INT,
    id_proveedor INT,
    id_unidad INT,
    codigo_barras VARCHAR(50) NOT NULL UNIQUE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_unidad) REFERENCES unidades(id_unidad)
);

-- Tabla: empleados
CREATE TABLE empleados (
    id_empleado INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL
);

-- Tabla: usuarios
CREATE TABLE usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL
);

-- Tabla: compras
CREATE TABLE compras (
    id_compra INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    id_categoria INT,
    id_unidad INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_unidad) REFERENCES unidades(id_unidad)
);

-- Tabla: detalles_compras
CREATE TABLE detalles_compras (
    id_detalle_compra INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_compra INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla: inventario
CREATE TABLE inventario (
    id_inventario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL UNIQUE,
    cantidad INT NOT NULL,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla: ventas
CREATE TABLE ventas (
    id_venta INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_empleado INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);

-- Tabla: detalle_ventas
CREATE TABLE detalle_ventas (
    id_detalle INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla: pagos
CREATE TABLE pagos (
    id_pago INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    metodo_pago ENUM('efectivo', 'tarjeta', 'transferencia') NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta)
);

-- Tabla: ventas_temporales
CREATE TABLE ventas_temporales (
    id_temp INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla: detalle_ventas_temporales
CREATE TABLE detalle_ventas_temporales (
    id_detalle INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_temp INT NOT NULL,
    id_producto INT NOT NULL,
    nombre_producto VARCHAR(255) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_temp) REFERENCES ventas_temporales(id_temp)
);







-- ORDEN CORRECTO DE INSERCIONES SEGÚN TU ESQUEMA Y DATOS ACTUALES

-- 1. CATEGORÍAS (ya existe, pero por si necesitas crearla)
INSERT INTO categorias (id_categoria, nombre) VALUES
(1, 'frituras');

-- 2. UNIDADES (ya existe, pero por si necesitas crearla)
INSERT INTO unidades (id_unidad, nombre) VALUES
(1, 'unidad');

-- 3. PROVEEDORES (ya existe, pero por si necesitas crearla)
INSERT INTO proveedores (id_proveedor, nombre, direccion, telefono, email) VALUES
(1, 'davicho', 'calle cipres', '9612798030', 'david@gmail');

-- 4. PRODUCTOS (NO incluyas los productos ya existentes en tu tabla para evitar duplicados)
-- Si quieres agregar más productos, cambia los valores de nombre, precio, stock, etc.
INSERT INTO productos (nombre, precio, stock, id_categoria, id_proveedor, id_unidad, codigo_barras) VALUES
('Rancheritos', 15, 20, 1, 1, 1, '5463633356'),
('Sabritas Clásicas', 16, 20, 1, 1, 1, '65545665'),
('Cheetos Torciditos', 14, 20, 1, 1, 1, '76436467435'),
('Ruffles Queso', 17, 20, 1, 1, 1, '7445565543'),
('Sabritones', 15, 20, 1, 1, 1, '436537755'),
('Chip´s Jalapeño', 17, 20, 1, 1, 1, '6525622566'),
('Doritos Nachos', 18, 20, 1, 1, 1, '36562652455'),
('Ruffles Limón', 17, 20, 1, 1, 1, '1234556674'),
('Paketaxo', 18, 20, 1, 1, 1, '65465445642'),
('Sabritas Adobadas', 16, 20, 1, 1, 1, '9086579684'),
('Cheetos Poffets', 14, 20, 1, 1, 1, '64365753556'),
('Barcel Chips Moradas', 17, 20, 1, 1, 1, '76456553566'),
('Runners', 15, 20, 1, 1, 1, '5436462623'),
('Totis', 14, 20, 1, 1, 1, '75456536653'),
('Ruffles BBQ', 17, 20, 1, 1, 1, '83558853643'),
('Sabritas Picositas', 16, 20, 1, 1, 1, '0675350647'),
('Cheetos Flamin Hot', 15, 20, 1, 1, 1, '01232673037'),
('Fritos', 13, 20, 1, 1, 1, '3892749299'),
('Takis Original', 15, 20, 1, 1, 1, '34562224524'),
('Ondas', 14, 20, 1, 1, 1, '3232542324');

-- 5. EMPLEADOS (primero empleados, después usuarios)
INSERT INTO empleados (id_empleado, nombre, cargo, salario) VALUES
(2, 'david', 'Gerente', 10000.00),
(3, 'Fabricio', 'bodeguero', 1500.00),
(4, 'Josue', 'Panaderia', 1000.00),
(5, 'Emilio', 'Cajero', 2000.00),
(6, 'Marco', 'Bodega', 3000.00);

-- 6. USUARIOS (usa los id_empleado de arriba, y NO repitas si ya existen)
INSERT INTO usuarios (id_usuario, id_empleado, username, password) VALUES
(1, 2, 'david', 'david1234'),
(3, 3, 'EDUARDO', 'ed2345'),
(4, 4, 'JosuePV', 'password'),
(5, 5, 'EmilioSA', 'password'),
(6, 6, 'MarcoFE', 'password');

-- 7. INVENTARIO
-- Inserta el stock inicial para los productos nuevos recién agregados
-- Si tus productos nuevos tienen id_producto consecutivos, por ejemplo del 41 al 60:
INSERT INTO inventario (id_producto, cantidad) VALUES
(41, 20),(42, 20),(43, 20),(44, 20),(45, 20),
(46, 20),(47, 20),(48, 20),(49, 20),(50, 20),
(51, 20),(52, 20),(53, 20),(54, 20),(55, 20),
(56, 20),(57, 20),(58, 20),(59, 20),(60, 20);

-- Si no sabes el id_producto puedes usar:
-- INSERT INTO inventario (id_producto, cantidad)
-- SELECT id_producto, stock FROM productos WHERE codigo_barras IN
-- ('5463633356','65545665','76436467435','7445565543','436537755','6525622566','36562652455','1234556674','65465445642','9086579684','64365753556','76456553566','5436462623','75456536653','83558853643','0675350647','01232673037','3892749299','34562224524','3232542324');